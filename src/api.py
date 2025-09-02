"""
ANISA Web API
Provides REST API endpoints for the ANISA Core Engine.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

import os
from fastapi import FastAPI, HTTPException, BackgroundTasks, Header, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core import ANISACore
from config import ANISAConfig
from models import (
    CulturalContext,
    CulturalRegion,
    CulturalVariant,
    TradeContext,
    ComplianceLevel,
    GTCEcosystemComponent,
)


# Pydantic models for API requests/responses
class QueryRequest(BaseModel):
    """Request model for cultural queries."""
    text: str = Field(..., description="The text to process", min_length=1, max_length=1000)
    language: str = Field(default="en", description="Language code", max_length=10)
    cultural_variant: Optional[str] = Field(default=None, description="Preferred cultural variant")


class QueryResponse(BaseModel):
    """Response model for cultural queries."""
    response_text: str = Field(..., description="The generated response")
    cultural_variant: str = Field(..., description="Cultural variant used")
    authenticity_score: float = Field(..., description="Authenticity score (0.0-1.0)")
    cultural_markers_used: List[str] = Field(..., description="Cultural markers identified")
    processing_time: float = Field(..., description="Processing time in seconds")
    cultural_context: Dict[str, Any] = Field(..., description="Detected cultural context")


class CulturalInsightsRequest(BaseModel):
    """Request model for cultural insights."""
    topic: str = Field(..., description="Topic to get insights for", min_length=1, max_length=100)


class CulturalInsightsResponse(BaseModel):
    """Response model for cultural insights."""
    topic: str = Field(..., description="The requested topic")
    insights: List[str] = Field(..., description="Cultural insights")
    processing_time: float = Field(..., description="Processing time in seconds")


class SystemStatusResponse(BaseModel):
    """Response model for system status."""
    status: str = Field(..., description="System status")
    uptime_seconds: float = Field(..., description="System uptime in seconds")
    total_queries: int = Field(..., description="Total queries processed")
    success_rate: float = Field(..., description="Success rate (0.0-1.0)")
    average_response_time: float = Field(..., description="Average response time in seconds")
    timestamp: datetime = Field(..., description="Status timestamp")


class PerformanceMetricsResponse(BaseModel):
    """Response model for performance metrics."""
    total_queries: int = Field(..., description="Total queries processed")
    successful_queries: int = Field(..., description="Successful queries")
    failed_queries: int = Field(..., description="Failed queries")
    average_response_time: float = Field(..., description="Average response time in seconds")
    start_time: datetime = Field(..., description="System start time")


# PANX integration models
class PanxToolFunction(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class PanxAnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    language: str = Field(default="en", max_length=10)
    region_hint: Optional[str] = Field(default=None, description="Optional region hint")


class PanxAnalyzeResponse(BaseModel):
    authenticity_score: float
    detected_region: str
    detected_variant: str
    compliance_notes: List[str] = []
    recommendations: List[str] = []


class PanxVerificationEvent(BaseModel):
    event_type: str = Field(..., description="Verification event type (e.g., export_permit_issued)")
    region: str = Field(..., description="Cultural region value")
    trade_context: str = Field(..., description="Trade context value")
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Evidence package")


class PanxConsensusHint(BaseModel):
    recommended_validators: List[str]
    minimum_consensus: float
    cultural_risks: List[str] = []
    compliance_notes: List[str] = []
    region: str
    variant: str


# Initialize FastAPI app
app = FastAPI(
    title="ANISA API",
    description="Authentic Native Intelligence Systematically Applied - Cultural Intelligence API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ANISA core
config = ANISAConfig()
core = ANISACore(config)
logger = logging.getLogger(__name__)

# Simple API key auth (SGX placeholder)
ANISA_API_KEY = os.environ.get("ANISA_API_KEY")


async def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Verify API key if configured. Acts as SGX placeholder for service auth.

    If ANISA_API_KEY env var is set, require header X-API-Key to match.
    """
    if ANISA_API_KEY:
        if not x_api_key or x_api_key != ANISA_API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized: invalid API key")


def publish_event(event_name: str, payload: Dict[str, Any]) -> None:
    """Telemetry hook for Veritas adapter.

    Currently logs; can be replaced with a sink (HTTP, Kafka, etc.).
    """
    try:
        logger.info(f"telemetry.event={event_name} payload={payload}")
    except Exception:  # pragma: no cover
        pass


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("ANISA API starting up...")
    logger.info(f"Configuration: {config.to_dict()}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("ANISA API shutting down...")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "ANISA - Authentic Native Intelligence Systematically Applied",
        "version": "0.1.0",
        "status": "operational"
    }


@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/v1/query", response_model=QueryResponse, dependencies=[Depends(verify_api_key)])
async def process_cultural_query(request: QueryRequest, http_response: Response):
    """Process a cultural query and return an intelligent response."""
    start_time = datetime.now()
    
    try:
        # Process the query
        response_obj = await core.process_cultural_query(request.text, request.language)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Get cultural context
        context = await core.detect_cultural_context(request.text, request.language)
        # Set helpful response headers for gateways/policies
        http_response.headers["X-ANISA-Region"] = context.region.value
        http_response.headers["X-ANISA-Variant"] = context.variant.value
        http_response.headers["X-ANISA-Authenticity"] = f"{response_obj.authenticity_score:.2f}"

        # Telemetry event
        publish_event(
            "anisa.query.processed",
            {
                "language": request.language,
                "region": context.region.value,
                "variant": context.variant.value,
                "processing_time": processing_time,
                "authenticity_score": response_obj.authenticity_score,
            },
        )

        return QueryResponse(
            response_text=response_obj.response_text,
            cultural_variant=response_obj.cultural_variant.value,
            authenticity_score=response_obj.authenticity_score,
            cultural_markers_used=response_obj.cultural_markers_used,
            processing_time=processing_time,
            cultural_context={
                "region": context.region.value,
                "variant": context.variant.value,
                "language": context.language,
                "dialect": context.dialect
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/api/v1/insights", response_model=CulturalInsightsResponse, dependencies=[Depends(verify_api_key)])
async def get_cultural_insights(request: CulturalInsightsRequest):
    """Get cultural insights for a given topic."""
    start_time = datetime.now()
    
    try:
        insights = await core.get_cultural_insights(request.topic)
        processing_time = (datetime.now() - start_time).total_seconds()

        publish_event(
            "anisa.insights.generated",
            {"topic": request.topic, "processing_time": processing_time, "count": len(insights)},
        )
        
        return CulturalInsightsResponse(
            topic=request.topic,
            insights=insights,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting insights: {str(e)}")


@app.get("/api/v1/status", response_model=SystemStatusResponse, dependencies=[Depends(verify_api_key)])
async def get_system_status():
    """Get the current system status."""
    try:
        status = core.get_system_status()
        return SystemStatusResponse(
            status=status["status"],
            uptime_seconds=status["uptime_seconds"],
            total_queries=status["total_queries"],
            success_rate=status["success_rate"],
            average_response_time=status["average_response_time"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting system status: {str(e)}")


@app.get("/api/v1/metrics", response_model=PerformanceMetricsResponse, dependencies=[Depends(verify_api_key)])
async def get_performance_metrics():
    """Get performance metrics."""
    try:
        metrics = core.get_performance_metrics()
        return PerformanceMetricsResponse(
            total_queries=metrics["total_queries"],
            successful_queries=metrics["successful_queries"],
            failed_queries=metrics["failed_queries"],
            average_response_time=metrics["average_response_time"],
            start_time=metrics["start_time"]
        )
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting metrics: {str(e)}")


@app.post("/api/v1/metrics/reset", dependencies=[Depends(verify_api_key)])
async def reset_metrics():
    """Reset performance metrics."""
    try:
        core.reset_metrics()
        return {"message": "Metrics reset successfully"}
        
    except Exception as e:
        logger.error(f"Error resetting metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Error resetting metrics: {str(e)}")


@app.get("/api/v1/variants", response_model=List[Dict[str, str]], dependencies=[Depends(verify_api_key)])
async def get_cultural_variants():
    """Get available cultural variants."""
    return [
        {"value": variant.value, "name": variant.name, "description": f"{variant.name} cultural approach"}
        for variant in CulturalVariant
    ]


@app.get("/api/v1/regions", response_model=List[Dict[str, str]], dependencies=[Depends(verify_api_key)])
async def get_cultural_regions():
    """Get available cultural regions."""
    return [
        {"value": region.value, "name": region.name, "description": f"{region.name} cultural region"}
        for region in CulturalRegion
    ]


@app.post("/api/v1/demo", dependencies=[Depends(verify_api_key)])
async def run_demo():
    """Run a demonstration of ANISA capabilities."""
    try:
        demo_queries = [
            "How can I build a strong community?",
            "What's the best way to solve problems creatively?",
            "How do I build trust in relationships?",
            "What's the smart way to handle challenges?",
            "How can I use my network effectively?"
        ]
        
        results = []
        for query in demo_queries:
            try:
                response = await core.process_cultural_query(query, "en")
                context = await core.detect_cultural_context(query, "en")
                
                results.append({
                    "query": query,
                    "response": response.response_text[:100] + "...",
                    "cultural_variant": response.cultural_variant.value,
                    "authenticity_score": response.authenticity_score,
                    "detected_region": context.region.value
                })
                
            except Exception as e:
                results.append({
                    "query": query,
                    "error": str(e)
                })
        
        return {
            "message": "Demo completed",
            "total_queries": len(demo_queries),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error running demo: {e}")
        raise HTTPException(status_code=500, detail=f"Error running demo: {str(e)}")


@app.get("/api/v1/tool/describe", dependencies=[Depends(verify_api_key)])
async def describe_panx_tool() -> Dict[str, Any]:
    """PANX tool descriptor for ANISA cultural query service.

    Provides a stable contract PANX can use to invoke ANISA.
    """
    return {
        "name": "anisa.cultural_intelligence",
        "version": "1.0",
        "description": "Cultural analysis, event assessment hints, and query generation for GTCX.",
        "auth": {"type": "api_key", "in": "header", "name": "X-API-Key"},
        "functions": [
            {
                "name": "query",
                "method": "POST",
                "path": "/api/v1/query",
                "input_schema": {
                    "type": "object",
                    "required": ["text"],
                    "properties": {
                        "text": {"type": "string", "minLength": 1, "maxLength": 1000},
                        "language": {"type": "string", "default": "en", "maxLength": 10},
                        "cultural_variant": {"type": "string"},
                    },
                },
                "output_schema": {"type": "object"},
            },
            {
                "name": "analyze",
                "method": "POST",
                "path": "/api/v1/panx/analyze",
                "input_schema": {
                    "type": "object",
                    "required": ["text"],
                    "properties": {
                        "text": {"type": "string", "minLength": 1, "maxLength": 2000},
                        "language": {"type": "string", "default": "en", "maxLength": 10},
                        "region_hint": {"type": "string"},
                    },
                },
                "output_schema": {"type": "object"},
            },
            {
                "name": "event_assess",
                "method": "POST",
                "path": "/api/v1/panx/event/assess",
                "input_schema": {
                    "type": "object",
                    "required": ["event_type", "region", "trade_context"],
                    "properties": {
                        "event_type": {"type": "string"},
                        "region": {"type": "string"},
                        "trade_context": {"type": "string"},
                        "evidence": {"type": "object"},
                    },
                },
                "output_schema": {"type": "object"},
            },
        ],
    }


@app.post("/api/v1/panx/analyze", response_model=PanxAnalyzeResponse, dependencies=[Depends(verify_api_key)])
async def panx_analyze(req: PanxAnalyzeRequest):
    """Analyze text for PANX: detect region/variant, compute authenticity, return notes."""
    try:
        # Detect context
        context = await core.detect_cultural_context(
            req.text,
            TradeContext.COMPLIANCE,
            ComplianceLevel.BASIC,
            [GTCEcosystemComponent.PANX_ORACLE, GTCEcosystemComponent.GCI_COMPLIANCE],
        )

        # Generate response to obtain authenticity score and notes
        response_obj = await core.process_cultural_query(
            req.text,
            TradeContext.COMPLIANCE,
            ComplianceLevel.BASIC,
            [GTCEcosystemComponent.PANX_ORACLE],
        )

        return PanxAnalyzeResponse(
            authenticity_score=response_obj.authenticity_score,
            detected_region=context.region.value,
            detected_variant=context.variant.value,
            compliance_notes=response_obj.compliance_notes,
            recommendations=response_obj.gtcx_recommendations,
        )
    except Exception as e:
        logger.error(f"Error in PANX analyze: {e}")
        raise HTTPException(status_code=500, detail=f"Error in PANX analyze: {str(e)}")


@app.post("/api/v1/panx/event/assess", response_model=PanxConsensusHint, dependencies=[Depends(verify_api_key)])
async def panx_event_assess(evt: PanxVerificationEvent):
    """Assess a PANX verification event and return consensus hints."""
    try:
        # Heuristic mapping for recommended validators and thresholds
        event = evt.event_type.lower()
        if event in {"export_permit_issued", "customs_clearance"}:
            recommended = ["government", "enterprise"]
            min_consensus = 0.75
        elif event in {"payment_released", "settlement_completed"}:
            recommended = ["enterprise", "community"]
            min_consensus = 0.80
        else:
            recommended = ["government", "enterprise", "community", "academic"]
            min_consensus = 0.67

        # Derive region/variant basics
        try:
            region_enum = CulturalRegion(evt.region)
        except Exception:
            region_enum = CulturalRegion.NORTH_AMERICA
        variant = {
            CulturalRegion.WEST_AFRICA: "ubuntu",
            CulturalRegion.SOUTH_ASIA: "jugaad",
            CulturalRegion.EAST_ASIA: "guanxi",
            CulturalRegion.LATIN_AMERICA: "jeitinho",
            CulturalRegion.MIDDLE_EAST: "wasta",
            CulturalRegion.NORTH_AMERICA: "individualism",
            CulturalRegion.EUROPE: "collectivism",
        }.get(region_enum, "individualism")

        # Simple cultural risks based on sparse evidence
        risks: List[str] = []
        if "dispute" in event:
            risks.append("Potential dispute escalation; ensure community validation")
        if evt.evidence and "custody" not in evt.evidence.keys():
            risks.append("Missing custody evidence; require VaultMark reference")

        notes: List[str] = []
        if evt.trade_context.lower() == TradeContext.COMPLIANCE.value:
            notes.append("Prioritize regulatory and cultural compliance checks")

        return PanxConsensusHint(
            recommended_validators=recommended,
            minimum_consensus=min_consensus,
            cultural_risks=risks,
            compliance_notes=notes,
            region=region_enum.value,
            variant=variant,
        )
    except Exception as e:
        logger.error(f"Error in PANX event assess: {e}")
        raise HTTPException(status_code=500, detail=f"Error in PANX event assess: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
