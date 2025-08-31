#!/usr/bin/env python3
"""
Simple ANISA Tests
Basic tests that match the actual implementation.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.models import CulturalContext, CulturalRegion, CulturalVariant
from src.config import ANISAConfig
from src.core import ANISACore
from src.services import CulturalAuthenticationService, NativeLanguageService, IntelligenceService


class TestANISAModels:
    """Test ANISA data models."""
    
    def test_cultural_context_creation(self):
        """Test creating a cultural context."""
        context = CulturalContext(
            region=CulturalRegion.WEST_AFRICA,
            variant=CulturalVariant.UBUNTU,
            language="en"
        )
        assert context.region == CulturalRegion.WEST_AFRICA
        assert context.variant == CulturalVariant.UBUNTU
        assert context.language == "en"
        assert context.dialect is None
        assert context.metadata == {}
    
    def test_cultural_context_with_optional_fields(self):
        """Test creating a cultural context with optional fields."""
        context = CulturalContext(
            region=CulturalRegion.SOUTH_ASIA,
            variant=CulturalVariant.JUGAAD,
            language="hi",
            dialect="hindi",
            metadata={"formality": "formal"}
        )
        assert context.dialect == "hindi"
        assert context.metadata["formality"] == "formal"
    
    def test_cultural_region_enum(self):
        """Test cultural region enum values."""
        assert CulturalRegion.WEST_AFRICA.value == "west_africa"
        assert CulturalRegion.SOUTH_ASIA.value == "south_asia"
        assert CulturalRegion.EAST_ASIA.value == "east_asia"
        assert CulturalRegion.LATIN_AMERICA.value == "latin_america"
        assert CulturalRegion.MIDDLE_EAST.value == "middle_east"
    
    def test_cultural_variant_enum(self):
        """Test cultural variant enum values."""
        assert CulturalVariant.UBUNTU.value == "ubuntu"
        assert CulturalVariant.JUGAAD.value == "jugaad"
        assert CulturalVariant.GUANXI.value == "guanxi"
        assert CulturalVariant.JEITINHO.value == "jeitinho"
        assert CulturalVariant.WASTA.value == "wasta"


class TestANISAConfig:
    """Test ANISA configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ANISAConfig()
        assert config.min_authenticity_score == 0.7
        assert config.max_cultural_markers == 10
        assert config.enable_multilingual is True
        assert config.max_concurrent_requests == 100
        assert config.request_timeout == 30.0
        assert config.log_format == "json"
        assert config.default_variant == "ubuntu"
        assert config.enable_variant_switching is True
        assert config.variant_confidence_threshold == 0.8
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ANISAConfig(
            min_authenticity_score=0.9,
            max_cultural_markers=20,
            enable_multilingual=False
        )
        assert config.min_authenticity_score == 0.9
        assert config.max_cultural_markers == 20
        assert config.enable_multilingual is False
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test valid values
        config = ANISAConfig(min_authenticity_score=0.5)
        assert config.min_authenticity_score == 0.5
        
        # Test boundary values
        config = ANISAConfig(min_authenticity_score=1.0)
        assert config.min_authenticity_score == 1.0


class TestANISACore:
    """Test ANISA core functionality."""
    
    def test_core_initialization(self):
        """Test ANISA core initialization."""
        config = ANISAConfig()
        core = ANISACore(config)
        
        assert core.config is not None
        assert core.auth_service is not None
        assert core.lang_service is not None
        assert core.intel_service is not None
        assert hasattr(core, 'logger')
    
    def test_core_has_required_methods(self):
        """Test that core has required methods."""
        config = ANISAConfig()
        core = ANISACore(config)
        
        assert hasattr(core, 'detect_cultural_context')
        assert hasattr(core, 'process_cultural_query')
        assert hasattr(core, 'get_system_status')
        assert hasattr(core, 'get_performance_metrics')


class TestANISAServices:
    """Test ANISA service classes."""
    
    def test_authentication_service_creation(self):
        """Test authentication service creation."""
        config = ANISAConfig()
        service = CulturalAuthenticationService(config)
        assert service is not None
        assert service.config is not None
    
    def test_language_service_creation(self):
        """Test language service creation."""
        config = ANISAConfig()
        service = NativeLanguageService(config)
        assert service is not None
        assert service.config is not None
    
    def test_intelligence_service_creation(self):
        """Test intelligence service creation."""
        config = ANISAConfig()
        service = IntelligenceService(config)
        assert service is not None
        assert service.config is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
