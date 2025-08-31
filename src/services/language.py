"""
Native Language Service
"""

import logging
from typing import List, Dict, Any
from ..models import CulturalContext, NativeUnderstanding, CulturalRegion, CulturalVariant
from ..config import ANISAConfig


class NativeLanguageService:
    """Service for processing native languages and understanding cultural context."""

    def __init__(self, config: ANISAConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Cultural insights for each variant
        self.cultural_insights = {
            CulturalVariant.UBUNTU: [
                "Community-first approach",
                "Collective decision making",
                "Respect for elders and tradition",
                "Harmony and balance"
            ],
            CulturalVariant.JUGAAD: [
                "Creative problem solving",
                "Resource optimization",
                "Innovation through constraints",
                "Adaptability and flexibility"
            ],
            CulturalVariant.GUANXI: [
                "Relationship building",
                "Trust and reciprocity",
                "Face and honor",
                "Long-term connections"
            ],
            CulturalVariant.JEITINHO: [
                "Creative workarounds",
                "Flexible solutions",
                "Smart problem solving",
                "Adaptability to situations"
            ],
            CulturalVariant.WASTA: [
                "Using connections and influence",
                "Helping others through networks",
                "Building social capital",
                "Reciprocal assistance"
            ]
        }

        self.logger.info("Native Language Service initialized")

    async def process_native_language(self, user_input: str, cultural_context: CulturalContext) -> NativeUnderstanding:
        """Process native language and extract cultural understanding."""
        try:
            # Extract cultural insights
            insights = self._extract_cultural_insights(user_input, cultural_context)

            # Analyze contextual meaning
            contextual_meaning = self._analyze_contextual_meaning(user_input, cultural_context)

            # Identify cultural nuances
            cultural_nuances = self._identify_cultural_nuances(user_input, cultural_context)

            # Detect trust indicators
            trust_indicators = self._detect_trust_indicators(user_input, cultural_context)

            return NativeUnderstanding(
                cultural_insights=insights,
                contextual_meaning=contextual_meaning,
                cultural_nuances=cultural_nuances,
                trust_indicators=trust_indicators
            )

        except Exception as e:
            self.logger.error(f"Error processing native language: {e}")
            return NativeUnderstanding(
                cultural_insights=["Error processing language"],
                contextual_meaning={"error": str(e)},
                cultural_nuances=["Unable to detect nuances"],
                trust_indicators=["Unable to detect trust indicators"]
            )

    async def detect_language(self, text: str) -> str:
        """Detect the primary language of the input text."""
        try:
            # Simple detection for now
            if any(word in text.lower() for word in ["the", "and", "or", "but", "in", "on", "at"]):
                return "en"
            elif any(word in text.lower() for word in ["le", "la", "les", "un", "une", "des"]):
                return "fr"
            elif any(word in text.lower() for word in ["el", "la", "los", "las", "un", "una"]):
                return "es"
            else:
                return "en"  # Default to English

        except Exception as e:
            self.logger.error(f"Error detecting language: {e}")
            return "en"

    async def detect_dialect(self, text: str, region: CulturalRegion) -> str:
        """Detect specific dialect within a cultural region."""
        try:
            if not self.config.enable_dialect_detection:
                return None

            # Simple dialect detection
            if region == CulturalRegion.WEST_AFRICA:
                if any(word in text.lower() for word in ["una", "dem", "wey", "dey"]):
                    return "pidgin"
                elif any(word in text.lower() for word in ["ẹ", "ọ", "ṣe", "wà"]):
                    return "yoruba"

            return None

        except Exception as e:
            self.logger.error(f"Error detecting dialect: {e}")
            return None

    def _extract_cultural_insights(self, text: str, context: CulturalContext) -> List[str]:
        """Extract cultural insights from the text."""
        insights = []

        if context.variant in self.cultural_insights:
            text_lower = text.lower()
            for insight in self.cultural_insights[context.variant]:
                if self._insight_matches_text(insight, text_lower):
                    insights.append(insight)

        # Add general insights
        if "community" in text.lower() or "together" in text.lower():
            insights.append("Collective orientation detected")

        if "creative" in text.lower() or "solution" in text.lower():
            insights.append("Problem-solving approach detected")

        return insights

    def _analyze_contextual_meaning(self, text: str, context: CulturalContext) -> Dict[str, Any]:
        """Analyze the contextual meaning of the text."""
        analysis = {
            "text_length": len(text),
            "word_count": len(text.split()),
            "language": context.language,
            "region": context.region.value,
            "variant": context.variant.value
        }

        # Analyze sentiment
        positive_words = ["good", "great", "excellent", "wonderful", "amazing", "helpful"]
        negative_words = ["bad", "terrible", "awful", "horrible", "difficult", "problem"]

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            analysis["sentiment"] = "positive"
        elif negative_count > positive_count:
            analysis["sentiment"] = "negative"
        else:
            analysis["sentiment"] = "neutral"

        return analysis

    def _identify_cultural_nuances(self, text: str, context: CulturalContext) -> List[str]:
        """Identify cultural nuances in the text."""
        nuances = []
        text_lower = text.lower()

        # Check for cultural-specific expressions
        if context.variant == CulturalVariant.UBUNTU:
            if "village" in text_lower or "community" in text_lower:
                nuances.append("Community-focused expression")
            if "respect" in text_lower or "elder" in text_lower:
                nuances.append("Respect for tradition")

        elif context.variant == CulturalVariant.JUGAAD:
            if "creative" in text_lower or "solution" in text_lower:
                nuances.append("Innovation-focused expression")
            if "make do" in text_lower or "work with" in text_lower:
                nuances.append("Resource optimization")

        elif context.variant == CulturalVariant.GUANXI:
            if "relationship" in text_lower or "connection" in text_lower:
                nuances.append("Relationship-building expression")
            if "trust" in text_lower or "honor" in text_lower:
                nuances.append("Trust and honor focus")

        return nuances

    def _detect_trust_indicators(self, text: str, context: CulturalContext) -> List[str]:
        """Detect trust indicators in the text."""
        indicators = []
        text_lower = text.lower()

        # Trust-related keywords
        trust_keywords = ["trust", "believe", "faith", "confidence", "rely", "depend"]

        for keyword in trust_keywords:
            if keyword in text_lower:
                indicators.append(f"Trust indicator: {keyword}")

        # Cultural trust patterns
        if context.variant == CulturalVariant.UBUNTU:
            if "community" in text_lower and "together" in text_lower:
                indicators.append("Community trust pattern")

        elif context.variant == CulturalVariant.GUANXI:
            if "relationship" in text_lower and "long-term" in text_lower:
                indicators.append("Relationship trust pattern")

        return indicators

    def _insight_matches_text(self, insight: str, text: str) -> bool:
        """Check if a cultural insight is reflected in the text."""
        insight_keywords = {
            "Community-first approach": ["community", "together", "collective", "group", "village"],
            "Creative problem solving": ["creative", "solve", "problem", "solution", "innovative"],
            "Relationship building": ["relationship", "build", "connect", "network", "establish"],
            "Creative workarounds": ["creative", "workaround", "solution", "smart", "clever"],
            "Using connections and influence": ["connection", "influence", "network", "help", "support"]
        }

        if insight in insight_keywords:
            return any(keyword in text for keyword in insight_keywords[insight])

        return False
