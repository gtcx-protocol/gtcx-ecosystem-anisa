"""
ANISA Data Models
Defines the core data structures for cultural intelligence processing.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime

# GTCX Ecosystem Integration Enums
class GTCEcosystemComponent(Enum):
    """GTCX ecosystem components that ANISA can integrate with"""
    PANX_ORACLE = "panx_oracle"
    GCI_COMPLIANCE = "gci_compliance"
    TRADEPASS = "tradepass"
    GEOTAG = "geotag"
    VAULTMARK = "vaultmark"
    PVP_SETTLEMENT = "pvp_settlement"
    AGI_NETWORK = "agi_network"
    TERMINAL_INTERFACE = "terminal_interface"
    CRX_SGX = "crx_sgx"
    ASM_PATHWAYS = "asm_pathways"
    VIA_VXA = "via_vxa"

class CulturalComplianceFactor(Enum):
    """Cultural factors that affect GTCX compliance"""
    COMMUNITY_CONSENT = "community_consent"
    TRADITIONAL_PRACTICES = "traditional_practices"
    LOCAL_AUTHORITY = "local_authority"
    CULTURAL_SOVEREIGNTY = "cultural_sovereignty"
    COMMUNAL_DECISION_MAKING = "communal_decision_making"
    RELATIONSHIP_BASED_TRADE = "relationship_based_trade"
    INFORMAL_ECONOMY_INTEGRATION = "informal_economy_integration"

class GTCTradePhase(Enum):
    """Phases of GTCX trade lifecycle"""
    PRE_TRADE_VERIFICATION = "pre_trade_verification"
    COMPLIANCE_ASSESSMENT = "compliance_assessment"
    CULTURAL_AUTHENTICATION = "cultural_authentication"
    NEGOTIATION = "negotiation"
    SETTLEMENT = "settlement"
    POST_TRADE_MONITORING = "post_trade_monitoring"

# Existing enums with GTCX-specific enhancements
class CulturalRegion(Enum):
    """Cultural regions with GTCX trade context"""
    WEST_AFRICA = "west_africa"  # Ubuntu economics, ASM focus
    SOUTH_ASIA = "south_asia"    # Jugaad innovation, informal economy
    EAST_ASIA = "east_asia"      # Guanxi relationships, formal trade
    LATIN_AMERICA = "latin_america"  # Jeitinho flexibility, community mining
    MIDDLE_EAST = "middle_east"  # Wasta connections, traditional trade
    NORTH_AMERICA = "north_america"  # Individualism, regulatory compliance
    EUROPE = "europe"            # Collectivism, sustainability focus

class CulturalVariant(Enum):
    """Cultural variants with GTCX trade implications"""
    UBUNTU = "ubuntu"           # Community-first, shared prosperity
    JUGGAD = "jugaad"           # Innovative problem-solving, resource optimization
    GUANXI = "guanxi"           # Relationship-based trade, trust networks
    JEITINHO = "jeitinho"       # Flexible adaptation, creative solutions
    WASTA = "wasta"             # Connection-based access, traditional authority
    INDIVIDUALISM = "individualism"  # Self-reliance, regulatory compliance
    COLLECTIVISM = "collectivism"    # Group harmony, sustainability

class TradeContext(Enum):
    """GTCX-specific trade contexts"""
    COMPLIANCE = "compliance"           # Regulatory compliance verification
    NEGOTIATION = "negotiation"         # Trade agreement discussions
    DOCUMENTATION = "documentation"     # Trade document processing
    SETTLEMENT = "settlement"           # Payment and delivery coordination
    MONITORING = "monitoring"           # Post-trade compliance monitoring
    DISPUTE_RESOLUTION = "dispute_resolution"  # Cultural dispute mediation
    COMMUNITY_ENGAGEMENT = "community_engagement"  # Local stakeholder involvement

class ComplianceLevel(Enum):
    """GTCX compliance levels with cultural considerations"""
    BASIC = "basic"                     # Minimum regulatory compliance
    ENTERPRISE = "enterprise"           # Full enterprise compliance
    CULTURAL_PLUS = "cultural_plus"     # Cultural compliance enhancement
    COMMUNITY_VERIFIED = "community_verified"  # Community-validated compliance
    SOVEREIGN_ALIGNED = "sovereign_aligned"    # National sovereignty compliance

# Enhanced data models with GTCX integration
@dataclass
class CulturalContext:
    """Enhanced cultural context with GTCX integration"""
    region: CulturalRegion
    variant: CulturalVariant
    trade_context: TradeContext
    compliance_level: ComplianceLevel
    gtcx_components: List[GTCEcosystemComponent] = field(default_factory=list)
    cultural_compliance_factors: List[CulturalComplianceFactor] = field(default_factory=list)
    trade_phase: Optional[GTCTradePhase] = None
    sovereignty_requirements: Dict[str, Any] = field(default_factory=dict)
    community_stakeholders: List[str] = field(default_factory=list)

@dataclass
class CulturalAuthentication:
    """Enhanced cultural authentication with GTCX validation"""
    cultural_confidence: float
    compliance_confidence: float
    confidence_score: float
    detected_region: CulturalRegion
    detected_variant: CulturalVariant
    compliance_alignment: float
    gtcx_integration_score: float
    sovereignty_compliance: bool
    community_validation: bool
    cultural_markers: List[str] = field(default_factory=list)
    compliance_markers: List[str] = field(default_factory=list)
    gtcx_compatibility: Dict[GTCEcosystemComponent, float] = field(default_factory=dict)

@dataclass
class NativeUnderstanding:
    """Enhanced native understanding with GTCX insights"""
    language_confidence: float
    dialect_detected: str
    cultural_insights: List[str]
    trade_implications: List[str]
    compliance_notes: List[str]
    gtcx_recommendations: List[str]
    community_insights: List[str]
    sovereignty_considerations: List[str]
    risk_factors: List[str] = field(default_factory=list)
    opportunity_indicators: List[str] = field(default_factory=list)

@dataclass
class IntelligentResponse:
    """Enhanced intelligent response with GTCX integration"""
    response_text: str
    cultural_context: CulturalContext
    authenticity_score: float
    trade_context: TradeContext
    compliance_notes: List[str]
    gtcx_integration_hints: List[str]
    gtcx_recommendations: List[str]
    cultural_adaptation: Dict[str, Any]
    ecosystem_compatibility: Dict[GTCEcosystemComponent, Dict[str, Any]]
    sovereignty_preservation: Dict[str, Any]
    community_engagement: Dict[str, Any]
    headers: Dict[str, str] = field(default_factory=dict)

# GTCX-specific trade models
@dataclass
class GTCTradeQuery:
    """GTCX-specific trade query with cultural context"""
    query_text: str
    trade_phase: GTCTradePhase
    commodity_type: str
    source_region: CulturalRegion
    destination_region: CulturalRegion
    compliance_requirements: List[str]
    cultural_considerations: List[str]
    sovereignty_requirements: Dict[str, Any]
    community_stakeholders: List[str]
    gtcx_components: List[GTCEcosystemComponent]

@dataclass
class GTCTradeResponse:
    """GTCX-specific trade response with cultural intelligence"""
    trade_recommendations: List[str]
    cultural_adaptations: List[str]
    compliance_strategy: Dict[str, Any]
    community_engagement_plan: List[str]
    sovereignty_preservation_measures: List[str]
    gtcx_integration_plan: Dict[GTCEcosystemComponent, Dict[str, Any]]
    risk_mitigation: List[str]
    opportunity_optimization: List[str]
    cultural_authentication: CulturalAuthentication
    native_understanding: NativeUnderstanding
    intelligent_response: IntelligentResponse
