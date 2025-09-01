"""
ANISA Core Engine
Main orchestrator for cultural intelligence processing.
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from models import (
    CulturalContext, CulturalAuthentication, NativeUnderstanding, 
    IntelligentResponse, CulturalRegion, CulturalVariant
)
from config import ANISAConfig
from services import (
    CulturalAuthenticationService, NativeLanguageService, IntelligenceService
)


class ANISACore:
    """Main ANISA Core Engine for cultural intelligence processing."""
    
    def __init__(self, config: ANISAConfig):
        """Initialize the ANISA Core Engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize services
        self.auth_service = CulturalAuthenticationService(config)
        self.lang_service = NativeLanguageService(config)
        self.intel_service = IntelligenceService(config)
        
        # Performance tracking
        self.metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "average_response_time": 0.0,
            "start_time": datetime.now()
        }
        
        self.logger.info("ANISA Core Engine initialized successfully")
    
    async def process_cultural_query(
        self, 
        user_input: str, 
        language: str = "en"
    ) -> IntelligentResponse:
        """Process a cultural query and return an intelligent response."""
        start_time = time.time()
        self.metrics["total_queries"] += 1
        
        try:
            # Detect cultural context
            cultural_context = await self.detect_cultural_context(user_input, language)
            
            # Process native language
            native_understanding = await self.lang_service.process_native_language(
                user_input, cultural_context
            )
            
            # Authenticate cultural context
            auth_result = await self.auth_service.authenticate_cultural_context(
                user_input, cultural_context
            )
            
            # Generate intelligent response
            response = await self.intel_service.generate_cultural_response(
                user_input, cultural_context, native_understanding
            )
            
            # Update metrics
            response_time = time.time() - start_time
            self._update_metrics(response_time, True)
            
            self.logger.info(f"Query processed successfully in {response_time:.3f}s")
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            self._update_metrics(time.time() - start_time, False)
            
            # Return fallback response
            return await self._create_fallback_response(user_input, language)
    
    async def detect_cultural_context(self, user_input: str, language: str) -> CulturalContext:
        """Detect the cultural context from user input."""
        try:
            # Detect cultural region
            region = await self.auth_service.detect_cultural_region(user_input)
            
            # Map region to variant
            variant_mapping = {
                CulturalRegion.WEST_AFRICA: CulturalVariant.UBUNTU,
                CulturalRegion.SOUTH_ASIA: CulturalVariant.JUGAAD,
                CulturalRegion.EAST_ASIA: CulturalVariant.GUANXI,
                CulturalRegion.LATIN_AMERICA: CulturalVariant.JEITINHO,
                CulturalRegion.MIDDLE_EAST: CulturalVariant.WASTA
            }
            
            variant = variant_mapping.get(region, CulturalVariant.UBUNTU)
            
            # Detect dialect if enabled
            dialect = None
            if self.config.enable_dialect_detection:
                dialect = await self.lang_service.detect_dialect(user_input, region)
            
            return CulturalContext(
                region=region,
                variant=variant,
                language=language,
                dialect=dialect
            )
            
        except Exception as e:
            self.logger.error(f"Error detecting cultural context: {e}")
            # Return default context
            return CulturalContext(
                region=CulturalRegion.WEST_AFRICA,
                variant=CulturalVariant.UBUNTU,
                language=language
            )
    
    async def process_multilingual_query(
        self, 
        user_input: str, 
        source_language: str
    ) -> IntelligentResponse:
        """Process a query in its native language."""
        try:
            # Detect actual language if different from source
            detected_language = await self.lang_service.detect_language(user_input)
            actual_language = detected_language if detected_language != "en" else source_language
            
            # Process with detected language
            return await self.process_cultural_query(user_input, actual_language)
            
        except Exception as e:
            self.logger.error(f"Error processing multilingual query: {e}")
            return await self._create_fallback_response(user_input, source_language)
    
    async def get_cultural_insights(self, topic: str) -> List[str]:
        """Get cultural insights for a given topic."""
        try:
            # This would integrate with cultural knowledge base
            insights = [
                f"Cultural perspective on {topic}",
                f"Regional variations in {topic}",
                f"Traditional approaches to {topic}"
            ]
            return insights
            
        except Exception as e:
            self.logger.error(f"Error getting cultural insights: {e}")
            return [f"Unable to provide insights on {topic}"]
    
    async def validate_cultural_response(
        self, 
        response: IntelligentResponse, 
        context: CulturalContext
    ) -> CulturalAuthentication:
        """Validate the cultural authenticity of a response."""
        try:
            return await self.auth_service.validate_response_authenticity(response, context)
        except Exception as e:
            self.logger.error(f"Error validating response: {e}")
            return CulturalAuthentication(
                is_authentic=False,
                confidence_score=0.0,
                detected_markers=[],
                cultural_alignment=0.0,
                validation_errors=[f"Validation error: {str(e)}"]
            )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current system status."""
        uptime = datetime.now() - self.metrics["start_time"]
        
        return {
            "status": "operational",
            "uptime_seconds": uptime.total_seconds(),
            "total_queries": self.metrics["total_queries"],
            "success_rate": (
                self.metrics["successful_queries"] / max(self.metrics["total_queries"], 1)
            ),
            "average_response_time": self.metrics["average_response_time"]
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        return self.metrics.copy()
    
    def reset_metrics(self) -> None:
        """Reset performance metrics."""
        self.metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "average_response_time": 0.0,
            "start_time": datetime.now()
        }
        self.logger.info("Performance metrics reset")
    
    async def _create_fallback_response(self, user_input: str, language: str) -> IntelligentResponse:
        """Create a fallback response when processing fails."""
        fallback_text = f"I apologize, but I'm having trouble processing your request. Please try again."
        
        return IntelligentResponse(
            response_text=fallback_text,
            cultural_variant=CulturalVariant.UBUNTU,
            authenticity_score=0.5,
            cultural_markers_used=["fallback"],
            response_metadata={"is_fallback": True, "error": "Processing failed"}
        )
    
    def _update_metrics(self, response_time: float, success: bool) -> None:
        """Update performance metrics."""
        if success:
            self.metrics["successful_queries"] += 1
        else:
            self.metrics["failed_queries"] += 1
        
        # Update average response time
        total_queries = self.metrics["successful_queries"] + self.metrics["failed_queries"]
        current_avg = self.metrics["average_response_time"]
        self.metrics["average_response_time"] = (
            (current_avg * (total_queries - 1) + response_time) / total_queries
        )
