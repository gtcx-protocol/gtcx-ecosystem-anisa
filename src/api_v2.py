"""
ANISA Production API v2
Enhanced with database persistence, metrics, and PANX/Cortex integration
"""

import asyncio
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException, Header, Depends, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential

from core import ANISACore
from config import ANISAConfig
from database import get_db, init_db, CulturalContext as DBContext, CulturalInsight as DBInsight
from database import CulturalVerification, CulturalMetrics
from models import CulturalContext, CulturalRegion, CulturalVariant

# Metrics
request_count = Counter('anisa_requests_total', 'Total requests', ['endpoint', 'method', 'status'])
request_duration = Histogram('anisa_request_duration_seconds', 'Request duration', ['endpoint'])
cultural_analysis_count = Counter('anisa_cultural_analysis_total', 'Cultural analyses', ['region', 'variant'])

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ANISA API v2",
    description="Authentic Native Intelligence Systematically Applied - Production API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ANISA core
config = ANISAConfig()
core = ANISACore(config)

# API Configuration
ANISA_API_KEY = os.getenv("ANISA_API_KEY")
PANX_URL = os.getenv("PANX_URL", "http://panx:8081")
CORTEX_URL = os.getenv("CORTEX_URL", "http://cortex:8082")
PANX_API_KEY = os.getenv("PANX_API_KEY")
CORTEX_API_KEY = os.getenv("CORTEX_API_KEY")

# HTTP client for integrations
http_client = httpx.AsyncClient(timeout=30.0)


# Request/Response Models
class CulturalAnalysisRequest(BaseModel):
    """Request for cultural analysis"""
    text: str = Field(..., min_length=1, max_length=5000)
    language: str = Field(default="en", max_length=10)
    trade_context: Optional[str] = Field(default=None, max_length=100)
    region_hint: Optional[str] = Field(default=None, max_length=50)


class CulturalAnalysisResponse(BaseModel):
    """Response from cultural analysis"""
    analysis_id: str
    region: str
    variant: str
    confidence_score: float
    cultural_factors: Dict[str, Any]
    trade_implications: Dict[str, Any]
    recommendations: List[str]
    processing_time_ms: float


class PANXIntegrationRequest(BaseModel):
    """Request for PANX cultural weight calculation"""
    event_type: str
    lot_id: str
    validators: List[str]
    region: str
    trade_context: Optional[Dict[str, Any]] = None


class PANXIntegrationResponse(BaseModel):
    """Response with cultural weights for PANX"""
    cultural_weights: Dict[str, float]
    consensus_adjustment: float
    cultural_factors: List[str]
    recommendations: List[str]


# Middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add request ID to all requests"""
    request_id = request.headers.get("X-Request-Id", str(uuid4()))
    request.state.request_id = request_id
    
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    response.headers["X-Request-Id"] = request_id
    response.headers["X-Process-Time-Ms"] = str(process_time)
    
    # Log request
    logger.info(f"Request {request_id} - {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
    
    # Record metrics
    request_count.labels(
        endpoint=request.url.path,
        method=request.method,
        status=response.status_code
    ).inc()
    
    request_duration.labels(endpoint=request.url.path).observe(process_time / 1000)
    
    return response


# Authentication
async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> None:
    """Verify API key if configured"""
    if ANISA_API_KEY and x_api_key != ANISA_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# Startup/Shutdown
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("ANISA v2 starting up...")
    init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("ANISA v2 shutting down...")
    await http_client.aclose()


# Health & Metrics Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "anisa",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type="text/plain")


# Core API Endpoints
@app.post("/api/v2/analyze", response_model=CulturalAnalysisResponse, dependencies=[Depends(verify_api_key)])
async def analyze_cultural_context(
    request: CulturalAnalysisRequest,
    db: Session = Depends(get_db),
    x_request_id: Optional[str] = Header(None)
):
    """Analyze cultural context with database persistence"""
    start_time = time.time()
    
    try:
        # Perform cultural analysis
        context = await core.detect_cultural_context(request.text, request.language)
        insights = await core.generate_cultural_insights(request.text, context)
        
        # Store in database
        db_context = DBContext(
            text=request.text,
            language=request.language,
            region=context.region.value,
            variant=context.variant.value,
            confidence_score=insights.authenticity_score,
            cultural_markers=insights.cultural_markers_used,
            trade_context=request.trade_context
        )
        db.add(db_context)
        db.commit()
        
        db_insight = DBInsight(
            context_id=db_context.id,
            event_type=request.trade_context or "general",
            cultural_factors=insights.cultural_factors,
            recommendations=insights.recommendations,
            authenticity_score=insights.authenticity_score,
            trade_implications=insights.trade_implications
        )
        db.add(db_insight)
        db.commit()
        
        # Record metrics
        cultural_analysis_count.labels(
            region=context.region.value,
            variant=context.variant.value
        ).inc()
        
        # Forward to Cortex for analytics
        await forward_to_cortex({
            "event_type": "cultural_analysis",
            "analysis_id": str(db_context.id),
            "region": context.region.value,
            "variant": context.variant.value,
            "confidence_score": insights.authenticity_score,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        processing_time = (time.time() - start_time) * 1000
        
        return CulturalAnalysisResponse(
            analysis_id=str(db_context.id),
            region=context.region.value,
            variant=context.variant.value,
            confidence_score=insights.authenticity_score,
            cultural_factors=insights.cultural_factors,
            trade_implications=insights.trade_implications,
            recommendations=insights.recommendations,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in cultural analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v2/panx/cultural_weights", response_model=PANXIntegrationResponse, dependencies=[Depends(verify_api_key)])
async def get_cultural_weights_for_panx(
    request: PANXIntegrationRequest,
    db: Session = Depends(get_db)
):
    """Calculate cultural weights for PANX consensus"""
    try:
        # Determine cultural weights based on region and validators
        cultural_weights = calculate_cultural_weights(
            request.validators,
            request.region,
            request.event_type
        )
        
        # Calculate consensus adjustment
        consensus_adjustment = calculate_consensus_adjustment(
            request.region,
            request.event_type,
            request.trade_context
        )
        
        # Get cultural factors
        cultural_factors = get_cultural_factors(request.region, request.event_type)
        
        # Generate recommendations
        recommendations = generate_cultural_recommendations(
            request.region,
            request.event_type,
            request.validators
        )
        
        # Store verification record
        verification = CulturalVerification(
            panx_event_id=f"{request.event_type}_{request.lot_id}",
            lot_id=request.lot_id,
            validators=request.validators,
            cultural_weights=cultural_weights,
            consensus_adjustment=consensus_adjustment
        )
        db.add(verification)
        db.commit()
        
        return PANXIntegrationResponse(
            cultural_weights=cultural_weights,
            consensus_adjustment=consensus_adjustment,
            cultural_factors=cultural_factors,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Error calculating cultural weights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v2/cortex/forward")
async def forward_cultural_event(event: Dict[str, Any]):
    """Forward cultural events to Cortex"""
    return await forward_to_cortex(event)


# Helper Functions
def calculate_cultural_weights(validators: List[str], region: str, event_type: str) -> Dict[str, float]:
    """Calculate cultural weights for validators"""
    # Base weights
    weights = {v: 1.0 for v in validators}
    
    # Adjust based on cultural context
    if region == "africa" and "community" in validators:
        weights["community"] = 1.5  # Community has higher weight in Ubuntu culture
    if region == "asia" and "government" in validators:
        weights["government"] = 1.3  # Government has higher weight in hierarchical cultures
    
    # Normalize weights
    total = sum(weights.values())
    return {k: v/total for k, v in weights.items()}


def calculate_consensus_adjustment(region: str, event_type: str, trade_context: Optional[Dict]) -> float:
    """Calculate consensus threshold adjustment based on culture"""
    base_adjustment = 1.0
    
    # Cultural adjustments
    if region == "africa" and event_type in ["community_approval", "mining_rights"]:
        base_adjustment = 1.2  # Require higher consensus for community matters
    elif region == "asia" and event_type in ["export_permit", "trade_agreement"]:
        base_adjustment = 0.9  # Slightly lower threshold for trade efficiency
    
    return base_adjustment


def get_cultural_factors(region: str, event_type: str) -> List[str]:
    """Get relevant cultural factors"""
    factors = []
    
    if region == "africa":
        factors.extend(["ubuntu", "community_consensus", "elder_approval"])
    elif region == "asia":
        factors.extend(["guanxi", "face_preservation", "hierarchy_respect"])
    
    return factors


def generate_cultural_recommendations(region: str, event_type: str, validators: List[str]) -> List[str]:
    """Generate cultural recommendations"""
    recommendations = []
    
    if region == "africa" and "community" not in validators:
        recommendations.append("Consider including community representatives for better cultural alignment")
    
    if region == "asia" and event_type == "trade_agreement":
        recommendations.append("Ensure proper relationship building before formal negotiations")
    
    return recommendations


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def forward_to_cortex(event: Dict[str, Any]) -> Dict[str, str]:
    """Forward event to Cortex for analytics"""
    try:
        response = await http_client.post(
            f"{CORTEX_URL}/cortex/ingest",
            json={"events": [event]},
            headers={"X-API-Key": CORTEX_API_KEY} if CORTEX_API_KEY else {}
        )
        response.raise_for_status()
        return {"status": "forwarded", "cortex_response": response.json()}
    except Exception as e:
        logger.error(f"Failed to forward to Cortex: {e}")
        return {"status": "failed", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)
