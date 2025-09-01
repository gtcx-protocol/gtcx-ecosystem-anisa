"""
Cultural Authentication Service for GTCX Ecosystem
Provides cultural context authentication and region/trade context detection.
"""

import re
from typing import List, Dict, Any
from models import (
    CulturalContext, CulturalAuthentication, CulturalRegion, CulturalVariant,
    TradeContext, ComplianceLevel, GTCEcosystemComponent, CulturalComplianceFactor
)


class CulturalAuthenticationService:
    """
    Service for authenticating cultural context and detecting cultural regions/trade contexts
    with enhanced GTCX ecosystem integration.
    """
    
    def __init__(self):
        """Initialize the cultural authentication service."""
        # Enhanced cultural markers for GTCX trade contexts
        self.cultural_markers = {
            CulturalVariant.UBUNTU: [
                "community", "ubuntu", "together", "shared", "collective", "we", "us",
                "prosperity", "harmony", "unity", "cooperation", "mutual", "interconnected",
                "mining cooperative", "artisanal mining", "community consent", "traditional authority"
            ],
            CulturalVariant.JUGGAD: [
                "jugaad", "innovative", "creative", "resourceful", "make do", "frugal",
                "optimization", "efficiency", "problem-solving", "adaptation", "flexible",
                "informal economy", "street smart", "practical", "quick fix"
            ],
            CulturalVariant.GUANXI: [
                "guanxi", "relationship", "connection", "network", "trust", "face",
                "reciprocity", "obligation", "social capital", "business relationship",
                "personal connection", "mutual benefit", "long-term", "loyalty"
            ],
            CulturalVariant.JEITINHO: [
                "jeitinho", "flexible", "creative", "adaptable", "workaround", "solution",
                "practical", "resourceful", "community mining", "local adaptation",
                "cultural flexibility", "informal solutions"
            ],
            CulturalVariant.WASTA: [
                "wasta", "connection", "influence", "network", "relationship", "authority",
                "traditional", "respect", "honor", "social standing", "family ties",
                "business network", "cultural authority"
            ],
            CulturalVariant.INDIVIDUALISM: [
                "individual", "self-reliance", "autonomy", "independence", "personal",
                "regulatory", "compliance", "standardization", "efficiency", "professional",
                "formal", "structured", "rule-based"
            ],
            CulturalVariant.COLLECTIVISM: [
                "collective", "group", "harmony", "sustainability", "environmental",
                "social responsibility", "community", "shared values", "cooperation",
                "long-term thinking", "stewardship"
            ]
        }
        
        # GTCX-specific compliance markers
        self.compliance_markers = {
            TradeContext.COMPLIANCE: [
                "regulation", "compliance", "standard", "requirement", "audit", "verification",
                "certification", "approval", "authorization", "permit", "license",
                "regulatory", "legal", "policy", "guideline"
            ],
            TradeContext.NEGOTIATION: [
                "negotiate", "discuss", "agree", "terms", "conditions", "deal", "bargain",
                "settlement", "agreement", "contract", "partnership", "collaboration",
                "mutual", "compromise", "consensus"
            ],
            TradeContext.DOCUMENTATION: [
                "document", "certificate", "proof", "evidence", "record", "file",
                "registration", "verification", "attestation", "endorsement",
                "paperwork", "form", "application", "submission"
            ],
            TradeContext.SETTLEMENT: [
                "settle", "payment", "delivery", "transfer", "exchange", "transaction",
                "clearing", "settlement", "fulfillment", "completion", "finalize",
                "execute", "process", "complete"
            ],
            TradeContext.MONITORING: [
                "monitor", "track", "observe", "supervise", "oversee", "watch",
                "surveillance", "inspection", "audit", "review", "assessment",
                "evaluation", "check", "verify"
            ],
            TradeContext.DISPUTE_RESOLUTION: [
                "dispute", "conflict", "resolution", "mediation", "arbitration",
                "negotiation", "settlement", "agreement", "compromise", "reconciliation",
                "peace", "harmony", "understanding"
            ],
            TradeContext.COMMUNITY_ENGAGEMENT: [
                "community", "engagement", "participation", "consultation", "involvement",
                "stakeholder", "collaboration", "partnership", "cooperation", "dialogue",
                "communication", "outreach", "inclusion"
            ]
        }
        
        # Enhanced regional detection keywords
        self.regional_keywords = {
            CulturalRegion.WEST_AFRICA: [
                "ghana", "nigeria", "senegal", "mali", "burkina faso", "ivory coast",
                "togo", "benin", "niger", "chad", "cameroon", "ubuntu", "community",
                "artisanal mining", "gold mining", "cocoa", "traditional authority",
                "mining cooperative", "community consent", "shared prosperity"
            ],
            CulturalRegion.SOUTH_ASIA: [
                "india", "pakistan", "bangladesh", "sri lanka", "nepal", "bhutan",
                "jugaad", "innovative", "resourceful", "informal economy", "street smart",
                "practical", "adaptation", "flexible", "quick fix", "make do"
            ],
            CulturalRegion.EAST_ASIA: [
                "china", "japan", "korea", "taiwan", "hong kong", "singapore",
                "guanxi", "relationship", "connection", "network", "trust", "face",
                "reciprocity", "business relationship", "personal connection",
                "long-term", "loyalty", "social capital"
            ],
            CulturalRegion.LATIN_AMERICA: [
                "brazil", "mexico", "argentina", "chile", "peru", "colombia",
                "venezuela", "ecuador", "bolivia", "paraguay", "uruguay",
                "jeitinho", "flexible", "creative", "adaptable", "workaround",
                "community mining", "local adaptation", "cultural flexibility"
            ],
            CulturalRegion.MIDDLE_EAST: [
                "saudi arabia", "uae", "qatar", "kuwait", "bahrain", "oman",
                "jordan", "lebanon", "syria", "iraq", "iran", "egypt", "turkey",
                "wasta", "connection", "influence", "network", "relationship",
                "traditional authority", "social standing", "family ties"
            ],
            CulturalRegion.NORTH_AMERICA: [
                "united states", "canada", "usa", "america", "north america",
                "individual", "self-reliance", "autonomy", "independence",
                "regulatory", "compliance", "standardization", "efficiency",
                "professional", "formal", "structured", "rule-based"
            ],
            CulturalRegion.EUROPE: [
                "europe", "european union", "eu", "germany", "france", "italy",
                "spain", "netherlands", "belgium", "austria", "switzerland",
                "collective", "group", "harmony", "sustainability", "environmental",
                "social responsibility", "community", "shared values", "cooperation"
            ]
        }
    
    def detect_cultural_region(self, text: str) -> CulturalRegion:
        """
        Detect cultural region from text with enhanced GTCX context.
        
        Args:
            text: Text to analyze for cultural region
            
        Returns:
            Detected cultural region
        """
        text_lower = text.lower()
        
        # Count matches for each region
        region_scores = {}
        for region, keywords in self.regional_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            region_scores[region] = score
        
        # Return region with highest score, default to WEST_AFRICA for GTCX focus
        if max(region_scores.values()) == 0:
            return CulturalRegion.WEST_AFRICA  # Default for GTCX ASM focus
        
        return max(region_scores, key=region_scores.get)
    
    def detect_cultural_variant(self, text: str) -> CulturalVariant:
        """
        Detect cultural variant from text with enhanced GTCX context.
        
        Args:
            text: Text to analyze for cultural variant
            
        Returns:
            Detected cultural variant
        """
        text_lower = text.lower()
        
        # Count matches for each variant
        variant_scores = {}
        for variant, markers in self.cultural_markers.items():
            score = sum(1 for marker in markers if marker in text_lower)
            variant_scores[variant] = score
        
        # Return variant with highest score, default to UBUNTU for GTCX focus
        if max(variant_scores.values()) == 0:
            return CulturalVariant.UBUNTU  # Default for GTCX community focus
        
        return max(variant_scores, key=variant_scores.get)
    
    def detect_trade_context(self, text: str) -> TradeContext:
        """
        Detect trade context from text with GTCX-specific markers.
        
        Args:
            text: Text to analyze for trade context
            
        Returns:
            Detected trade context
        """
        text_lower = text.lower()
        
        # Count matches for each trade context
        context_scores = {}
        for context, markers in self.compliance_markers.items():
            score = sum(1 for marker in markers if marker in text_lower)
            context_scores[context] = score
        
        # Return context with highest score, default to COMPLIANCE for GTCX focus
        if max(context_scores.values()) == 0:
            return TradeContext.COMPLIANCE  # Default for GTCX compliance focus
        
        return max(context_scores, key=context_scores.get)
    
    async def authenticate_cultural_context(
        self, 
        text: str, 
        cultural_context: CulturalContext
    ) -> CulturalAuthentication:
        """
        Authenticate cultural context with enhanced GTCX validation.
        
        Args:
            text: Text to authenticate
            cultural_context: Cultural context to validate against
            
        Returns:
            CulturalAuthentication result with GTCX integration
        """
        text_lower = text.lower()
        
        # Detect cultural markers
        cultural_markers = self._detect_cultural_markers(text_lower, cultural_context.variant)
        
        # Detect compliance markers
        compliance_markers = self._detect_compliance_markers(text_lower, cultural_context.trade_context)
        
        # Calculate cultural confidence
        cultural_confidence = self._calculate_cultural_confidence(
            cultural_markers, cultural_context.variant
        )
        
        # Calculate compliance confidence
        compliance_confidence = self._calculate_compliance_confidence(
            compliance_markers, cultural_context.trade_context
        )
        
        # Calculate combined confidence score
        confidence_score = (cultural_confidence * 0.6) + (compliance_confidence * 0.4)
        
        # Determine GTCX integration score
        gtcx_integration_score = self._calculate_gtcx_integration_score(
            cultural_context, cultural_markers, compliance_markers
        )
        
        # Check sovereignty compliance
        sovereignty_compliance = self._check_sovereignty_compliance(
            cultural_context, text_lower
        )
        
        # Check community validation
        community_validation = self._check_community_validation(
            cultural_context, text_lower
        )
        
        # Calculate compliance alignment
        compliance_alignment = self._calculate_compliance_alignment(
            cultural_context, compliance_markers
        )
        
        # Determine GTCX component compatibility
        gtcx_compatibility = self._determine_gtcx_compatibility(
            cultural_context, cultural_markers, compliance_markers
        )
        
        return CulturalAuthentication(
            cultural_confidence=cultural_confidence,
            compliance_confidence=compliance_confidence,
            confidence_score=confidence_score,
            detected_region=cultural_context.region,
            detected_variant=cultural_context.variant,
            compliance_alignment=compliance_alignment,
            gtcx_integration_score=gtcx_integration_score,
            sovereignty_compliance=sovereignty_compliance,
            community_validation=community_validation,
            cultural_markers=cultural_markers,
            compliance_markers=compliance_markers,
            gtcx_compatibility=gtcx_compatibility
        )
    
    def _detect_cultural_markers(self, text: str, variant: CulturalVariant) -> List[str]:
        """Detect cultural markers in text."""
        markers = self.cultural_markers.get(variant, [])
        detected = [marker for marker in markers if marker in text]
        return detected
    
    def _detect_compliance_markers(self, text: str, trade_context: TradeContext) -> List[str]:
        """Detect compliance markers in text."""
        markers = self.compliance_markers.get(trade_context, [])
        detected = [marker for marker in markers if marker in text]
        return detected
    
    def _calculate_cultural_confidence(
        self, 
        cultural_markers: List[str], 
        variant: CulturalVariant
    ) -> float:
        """Calculate cultural confidence score."""
        total_markers = len(self.cultural_markers.get(variant, []))
        if total_markers == 0:
            return 0.5  # Default confidence
        
        return min(1.0, len(cultural_markers) / max(1, total_markers * 0.3))
    
    def _calculate_compliance_confidence(
        self, 
        compliance_markers: List[str], 
        trade_context: TradeContext
    ) -> float:
        """Calculate compliance confidence score."""
        total_markers = len(self.compliance_markers.get(trade_context, []))
        if total_markers == 0:
            return 0.5  # Default confidence
        
        return min(1.0, len(compliance_markers) / max(1, total_markers * 0.3))
    
    def _calculate_gtcx_integration_score(
        self, 
        cultural_context: CulturalContext,
        cultural_markers: List[str],
        compliance_markers: List[str]
    ) -> float:
        """Calculate GTCX integration score."""
        # Base score from cultural and compliance markers
        base_score = (len(cultural_markers) * 0.1) + (len(compliance_markers) * 0.1)
        
        # Bonus for GTCX component alignment
        component_bonus = len(cultural_context.gtcx_components) * 0.05
        
        # Bonus for cultural compliance factors
        compliance_bonus = len(cultural_context.cultural_compliance_factors) * 0.03
        
        return min(1.0, base_score + component_bonus + compliance_bonus)
    
    def _check_sovereignty_compliance(
        self, 
        cultural_context: CulturalContext, 
        text: str
    ) -> bool:
        """Check sovereignty compliance."""
        sovereignty_keywords = [
            "sovereignty", "national", "local", "community", "traditional",
            "authority", "consent", "consultation", "participation"
        ]
        
        has_sovereignty_keywords = any(keyword in text for keyword in sovereignty_keywords)
        has_sovereignty_requirements = bool(cultural_context.sovereignty_requirements)
        
        return has_sovereignty_keywords or has_sovereignty_requirements
    
    def _check_community_validation(
        self, 
        cultural_context: CulturalContext, 
        text: str
    ) -> bool:
        """Check community validation."""
        community_keywords = [
            "community", "stakeholder", "consultation", "participation",
            "cooperation", "collaboration", "inclusion", "engagement"
        ]
        
        has_community_keywords = any(keyword in text for keyword in community_keywords)
        has_community_stakeholders = bool(cultural_context.community_stakeholders)
        
        return has_community_keywords or has_community_stakeholders
    
    def _calculate_compliance_alignment(
        self, 
        cultural_context: CulturalContext,
        compliance_markers: List[str]
    ) -> float:
        """Calculate compliance alignment score."""
        # Base alignment from compliance markers
        base_alignment = min(1.0, len(compliance_markers) * 0.1)
        
        # Bonus for cultural compliance factors
        compliance_factor_bonus = len(cultural_context.cultural_compliance_factors) * 0.05
        
        # Bonus for appropriate compliance level
        level_bonus = 0.1 if cultural_context.compliance_level != ComplianceLevel.BASIC else 0.0
        
        return min(1.0, base_alignment + compliance_factor_bonus + level_bonus)
    
    def _determine_gtcx_compatibility(
        self, 
        cultural_context: CulturalContext,
        cultural_markers: List[str],
        compliance_markers: List[str]
    ) -> Dict[GTCEcosystemComponent, float]:
        """Determine GTCX component compatibility scores."""
        compatibility = {}
        
        for component in cultural_context.gtcx_components:
            score = 0.5  # Base score
            
            # PANX Oracle compatibility
            if component == GTCEcosystemComponent.PANX_ORACLE:
                if "community" in cultural_markers or "stakeholder" in compliance_markers:
                    score += 0.3
                if cultural_context.variant in [CulturalVariant.UBUNTU, CulturalVariant.COLLECTIVISM]:
                    score += 0.2
            
            # GCI Compliance compatibility
            elif component == GTCEcosystemComponent.GCI_COMPLIANCE:
                if len(compliance_markers) > 0:
                    score += 0.3
                if cultural_context.compliance_level != ComplianceLevel.BASIC:
                    score += 0.2
            
            # TradePass compatibility
            elif component == GTCEcosystemComponent.TRADEPASS:
                if "identity" in cultural_markers or "verification" in compliance_markers:
                    score += 0.3
                if cultural_context.variant in [CulturalVariant.GUANXI, CulturalVariant.WASTA]:
                    score += 0.2
            
            # ASM Pathways compatibility
            elif component == GTCEcosystemComponent.ASM_PATHWAYS:
                if "artisanal" in cultural_markers or "mining" in cultural_markers:
                    score += 0.4
                if cultural_context.region == CulturalRegion.WEST_AFRICA:
                    score += 0.3
            
            compatibility[component] = min(1.0, score)
        
        return compatibility

