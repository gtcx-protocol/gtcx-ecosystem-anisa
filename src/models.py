"""
ANISA Data Models
Defines the core data structures for cultural intelligence processing.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional


class CulturalRegion(Enum):
    """Cultural regions supported by ANISA."""
    WEST_AFRICA = "west_africa"
    SOUTH_ASIA = "south_asia"
    EAST_ASIA = "east_asia"
    LATIN_AMERICA = "latin_america"
    MIDDLE_EAST = "middle_east"


class CulturalVariant(Enum):
    """Cultural variants for different regions."""
    UBUNTU = "ubuntu"      # Southern Africa
    JUGAAD = "jugaad"      # South Asia
    GUANXI = "guanxi"      # East Asia
    JEITINHO = "jeitinho"  # Latin America
    WASTA = "wasta"        # Middle East


@dataclass
class CulturalContext:
    """Cultural context for processing requests."""
    region: CulturalRegion
    variant: CulturalVariant
    language: str
    dialect: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CulturalAuthentication:
    """Result of cultural authentication."""
    is_authentic: bool
    confidence_score: float
    detected_markers: List[str]
    cultural_alignment: float
    validation_errors: List[str] = field(default_factory=list)


@dataclass
class NativeUnderstanding:
    """Native language understanding results."""
    cultural_insights: List[str]
    contextual_meaning: Dict[str, Any]
    cultural_nuances: List[str]
    trust_indicators: List[str]


@dataclass
class IntelligentResponse:
    """Culturally intelligent response."""
    response_text: str
    cultural_variant: CulturalVariant
    authenticity_score: float
    cultural_markers_used: List[str]
    response_metadata: Dict[str, Any] = field(default_factory=dict)
