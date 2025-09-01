"""
Cultural Authentication Service
"""

import logging
from typing import List
from models import CulturalContext, CulturalAuthentication, CulturalRegion, CulturalVariant
from config import ANISAConfig


class CulturalAuthenticationService:
    """Service for authenticating cultural context."""

    def __init__(self, config: ANISAConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Cultural markers for each variant
        self.cultural_markers = {
            CulturalVariant.UBUNTU: ["community", "together", "village", "harmony", "respect"],
            CulturalVariant.JUGAAD: ["creative", "solution", "innovative", "resourceful", "smart"],
            CulturalVariant.GUANXI: ["relationship", "connection", "trust", "honor", "network"],
            CulturalVariant.JEITINHO: ["flexible", "creative", "smart", "solution", "workaround"],
            CulturalVariant.WASTA: ["connection", "influence", "network", "help", "support"]
        }

        self.logger.info("Cultural Authentication Service initialized")

    async def authenticate_cultural_context(self, user_input: str, cultural_context: CulturalContext) -> CulturalAuthentication:
        """Authenticate the cultural context of user input."""
        try:
            # Detect cultural markers
            detected_markers = self._detect_cultural_markers(user_input, cultural_context.variant)

            # Calculate confidence score
            confidence_score = min(1.0, len(detected_markers) / 3)

            # Check if authentic
            is_authentic = confidence_score >= self.config.min_authenticity_score

            validation_errors = []
            if not is_authentic:
                validation_errors.append(f"Insufficient cultural markers detected (score: {confidence_score:.2f})")

            return CulturalAuthentication(
                is_authentic=is_authentic,
                confidence_score=confidence_score,
                detected_markers=detected_markers,
                cultural_alignment=confidence_score,
                validation_errors=validation_errors
            )

        except Exception as e:
            self.logger.error(f"Error in cultural authentication: {e}")
            return CulturalAuthentication(
                is_authentic=False,
                confidence_score=0.0,
                detected_markers=[],
                cultural_alignment=0.0,
                validation_errors=[f"Authentication error: {str(e)}"]
            )

    async def detect_cultural_region(self, user_input: str) -> CulturalRegion:
        """Detect the cultural region from user input."""
        try:
            input_lower = user_input.lower()

            # Enhanced region detection with more specific keywords
            if any(word in input_lower for word in ["ubuntu", "village", "community", "harmony", "together", "collective", "elders", "tradition"]):
                return CulturalRegion.WEST_AFRICA
            elif any(word in input_lower for word in ["jugaad", "creative", "innovative", "resourceful", "constraints", "optimization", "adaptability"]):
                return CulturalRegion.SOUTH_ASIA
            elif any(word in input_lower for word in ["guanxi", "relationship", "connection", "trust", "honor", "face", "long-term", "reciprocity"]):
                return CulturalRegion.EAST_ASIA
            elif any(word in input_lower for word in ["jeitinho", "flexible", "smart", "workaround", "challenge", "situation", "unconventional", "personal"]):
                return CulturalRegion.LATIN_AMERICA
            elif any(word in input_lower for word in ["wasta", "influence", "network", "connections", "social capital", "assistance", "help"]):
                return CulturalRegion.MIDDLE_EAST
            else:
                return CulturalRegion.WEST_AFRICA  # Default

        except Exception as e:
            self.logger.error(f"Error detecting cultural region: {e}")
            return CulturalRegion.WEST_AFRICA

    async def validate_response_authenticity(self, response, context: CulturalContext) -> CulturalAuthentication:
        """Validate the cultural authenticity of a generated response."""
        try:
            # Simple validation
            marker_alignment = min(1.0, len(response.cultural_markers_used) / 3)
            confidence_score = (marker_alignment + response.authenticity_score) / 2
            is_authentic = response.authenticity_score >= self.config.min_authenticity_score

            return CulturalAuthentication(
                is_authentic=is_authentic,
                confidence_score=confidence_score,
                detected_markers=response.cultural_markers_used,
                cultural_alignment=marker_alignment,
                validation_errors=[]
            )

        except Exception as e:
            self.logger.error(f"Error validating response authenticity: {e}")
            return CulturalAuthentication(
                is_authentic=False,
                confidence_score=0.0,
                detected_markers=[],
                cultural_alignment=0.0,
                validation_errors=[f"Validation error: {str(e)}"]
            )

    def _detect_cultural_markers(self, text: str, variant: CulturalVariant) -> List[str]:
        """Detect cultural markers in the given text."""
        detected = []
        text_lower = text.lower()

        if variant in self.cultural_markers:
            for marker in self.cultural_markers[variant]:
                if marker in text_lower:
                    detected.append(f"keyword:{marker}")

        return detected
