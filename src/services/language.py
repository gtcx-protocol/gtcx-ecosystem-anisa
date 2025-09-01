"""
Native Language Service
"""

import logging
from typing import List, Dict, Any
from models import CulturalContext, NativeUnderstanding, CulturalRegion, CulturalVariant
from config import ANISAConfig
from models import TradeContext, GTCEcosystemComponent, CulturalComplianceFactor


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
            CulturalVariant.JUGGAD: [
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

            # Detect dialect
            dialect = await self.detect_dialect(user_input, cultural_context.region)

            # Generate trade implications
            trade_implications = self._generate_trade_implications(user_input, cultural_context)

            # Generate compliance notes
            compliance_notes = self._generate_compliance_notes(user_input, cultural_context)

            # Generate GTCX recommendations
            gtcx_recommendations = self._generate_gtcx_recommendations(user_input, cultural_context)

            # Generate community insights
            community_insights = self._generate_community_insights(user_input, cultural_context)

            # Generate sovereignty considerations
            sovereignty_considerations = self._generate_sovereignty_considerations(user_input, cultural_context)

            # Identify risk factors
            risk_factors = self._identify_risk_factors(user_input, cultural_context)

            # Identify opportunities
            opportunities = self._identify_opportunities(user_input, cultural_context)

            return NativeUnderstanding(
                language_confidence=0.85,  # Default confidence
                dialect_detected=dialect or "standard",
                cultural_insights=insights,
                trade_implications=trade_implications,
                compliance_notes=compliance_notes,
                gtcx_recommendations=gtcx_recommendations,
                community_insights=community_insights,
                sovereignty_considerations=sovereignty_considerations,
                risk_factors=risk_factors,
                opportunity_indicators=opportunities
            )

        except Exception as e:
            self.logger.error(f"Error processing native language: {e}")
            return NativeUnderstanding(
                language_confidence=0.0,
                dialect_detected="unknown",
                cultural_insights=["Error processing language"],
                trade_implications=["Unable to process trade implications"],
                compliance_notes=["Unable to process compliance notes"],
                gtcx_recommendations=["Unable to generate GTCX recommendations"],
                community_insights=["Unable to process community insights"],
                sovereignty_considerations=["Unable to process sovereignty considerations"],
                risk_factors=["Unable to identify risk factors"],
                opportunity_indicators=["Unable to identify opportunities"]
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

    def _generate_trade_implications(self, text: str, context: CulturalContext) -> List[str]:
        """Generate trade implications based on cultural context."""
        implications = []
        
        if context.trade_context == TradeContext.COMPLIANCE:
            implications.append("Focus on regulatory compliance and documentation")
        elif context.trade_context == TradeContext.NEGOTIATION:
            implications.append("Emphasize relationship building and trust")
        elif context.trade_context == TradeContext.DOCUMENTATION:
            implications.append("Ensure proper documentation and verification")
        
        if context.variant == CulturalVariant.UBUNTU:
            implications.append("Include community stakeholders in trade decisions")
        elif context.variant == CulturalVariant.GUANXI:
            implications.append("Build long-term business relationships")
        
        return implications

    def _generate_compliance_notes(self, text: str, context: CulturalContext) -> List[str]:
        """Generate compliance notes based on cultural context."""
        notes = []
        
        for factor in context.cultural_compliance_factors:
            if factor == CulturalComplianceFactor.COMMUNITY_CONSENT:
                notes.append("Require community consultation for compliance")
            elif factor == CulturalComplianceFactor.TRADITIONAL_PRACTICES:
                notes.append("Respect traditional practices in compliance")
            elif factor == CulturalComplianceFactor.LOCAL_AUTHORITY:
                notes.append("Include local authority in compliance process")
        
        return notes

    def _generate_gtcx_recommendations(self, text: str, context: CulturalContext) -> List[str]:
        """Generate GTCX-specific recommendations."""
        recommendations = []
        
        for component in context.gtcx_components:
            if component == GTCEcosystemComponent.ASM_PATHWAYS:
                recommendations.append("Use ASM Pathways for community-validated mining")
            elif component == GTCEcosystemComponent.GCI_COMPLIANCE:
                recommendations.append("Leverage GCI for cultural compliance scoring")
            elif component == GTCEcosystemComponent.PANX_ORACLE:
                recommendations.append("Utilize PANX Oracle for multi-stakeholder consensus")
        
        return recommendations

    def _generate_community_insights(self, text: str, context: CulturalContext) -> List[str]:
        """Generate community insights based on cultural context."""
        insights = []
        
        for stakeholder in context.community_stakeholders:
            if "traditional_authority" in stakeholder:
                insights.append("Respect traditional authority structures")
            elif "mining_cooperatives" in stakeholder:
                insights.append("Engage with mining cooperatives")
            elif "local_communities" in stakeholder:
                insights.append("Include local community perspectives")
        
        return insights

    def _generate_sovereignty_considerations(self, text: str, context: CulturalContext) -> List[str]:
        """Generate sovereignty considerations."""
        considerations = []
        
        for requirement, value in context.sovereignty_requirements.items():
            if value:
                if requirement == "data_residency":
                    considerations.append("Ensure data remains within national borders")
                elif requirement == "community_consultation":
                    considerations.append("Require community consultation for decisions")
                elif requirement == "cultural_preservation":
                    considerations.append("Preserve cultural practices and traditions")
        
        return considerations

    def _identify_risk_factors(self, text: str, context: CulturalContext) -> List[str]:
        """Identify cultural risk factors."""
        risks = []
        
        if context.variant == CulturalVariant.UBUNTU and "individual" in text.lower():
            risks.append("Individual approach may conflict with community values")
        
        if context.trade_context == TradeContext.COMPLIANCE and "flexible" in text.lower():
            risks.append("Flexible approach may not meet strict compliance requirements")
        
        return risks

    def _identify_opportunities(self, text: str, context: CulturalContext) -> List[str]:
        """Identify cultural opportunities."""
        opportunities = []
        
        if context.variant == CulturalVariant.UBUNTU and "community" in text.lower():
            opportunities.append("Strong community alignment for collective success")
        
        if context.variant == CulturalVariant.GUANXI and "relationship" in text.lower():
            opportunities.append("Relationship-based approach for long-term partnerships")
        
        return opportunities

    def _analyze_contextual_meaning(self, text: str, context: CulturalContext) -> Dict[str, Any]:
        """Analyze the contextual meaning of the text."""
        analysis = {
            "text_length": len(text),
            "word_count": len(text.split()),
            "region": context.region.value,
            "variant": context.variant.value,
            "trade_context": context.trade_context.value,
            "compliance_level": context.compliance_level.value
        }

        return analysis

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
