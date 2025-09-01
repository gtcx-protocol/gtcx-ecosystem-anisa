"""
ANISA Configuration
Manages configuration settings for the ANISA Core Engine.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ANISAConfig:
    """Configuration for ANISA Core Engine."""
    
    # Cultural Authentication Settings
    min_authenticity_score: float = 0.7
    enable_cultural_validation: bool = True
    max_cultural_markers: int = 10
    
    # Language Processing Settings
    enable_dialect_detection: bool = True
    supported_languages: list = field(default_factory=lambda: ["en", "fr", "es", "ar", "zh", "hi"])
    enable_multilingual: bool = True
    
    # Intelligence Settings
    max_response_length: int = 500
    enable_response_enhancement: bool = True
    response_temperature: float = 0.8
    
    # Performance Settings
    max_concurrent_requests: int = 100
    request_timeout: float = 30.0
    enable_caching: bool = True
    
    # Logging Settings
    log_level: str = "INFO"
    enable_structured_logging: bool = True
    log_format: str = "json"
    
    # Cultural Variant Settings
    default_variant: str = "ubuntu"
    enable_variant_switching: bool = True
    variant_confidence_threshold: float = 0.8
    
    @classmethod
    def from_environment(cls) -> "ANISAConfig":
        """Create configuration from environment variables."""
        return cls(
            min_authenticity_score=float(os.getenv("ANISA_MIN_AUTHENTICITY_SCORE", "0.7")),
            enable_cultural_validation=os.getenv("ANISA_ENABLE_CULTURAL_VALIDATION", "true").lower() == "true",
            max_cultural_markers=int(os.getenv("ANISA_MAX_CULTURAL_MARKERS", "10")),
            enable_dialect_detection=os.getenv("ANISA_ENABLE_DIALECT_DETECTION", "true").lower() == "true",
            supported_languages=os.getenv("ANISA_SUPPORTED_LANGUAGES", "en,fr,es,ar,zh,hi").split(","),
            enable_multilingual=os.getenv("ANISA_ENABLE_MULTILINGUAL", "true").lower() == "true",
            max_response_length=int(os.getenv("ANISA_MAX_RESPONSE_LENGTH", "500")),
            enable_response_enhancement=os.getenv("ANISA_ENABLE_RESPONSE_ENHANCEMENT", "true").lower() == "true",
            response_temperature=float(os.getenv("ANISA_RESPONSE_TEMPERATURE", "0.8")),
            max_concurrent_requests=int(os.getenv("ANISA_MAX_CONCURRENT_REQUESTS", "100")),
            request_timeout=float(os.getenv("ANISA_REQUEST_TIMEOUT", "30.0")),
            enable_caching=os.getenv("ANISA_ENABLE_CACHING", "true").lower() == "true",
            log_level=os.getenv("ANISA_LOG_LEVEL", "INFO"),
            enable_structured_logging=os.getenv("ANISA_ENABLE_STRUCTURED_LOGGING", "true").lower() == "true",
            log_format=os.getenv("ANISA_LOG_FORMAT", "json"),
            default_variant=os.getenv("ANISA_DEFAULT_VARIANT", "ubuntu"),
            enable_variant_switching=os.getenv("ANISA_ENABLE_VARIANT_SWITCHING", "true").lower() == "true",
            variant_confidence_threshold=float(os.getenv("ANISA_VARIANT_CONFIDENCE_THRESHOLD", "0.8"))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "min_authenticity_score": self.min_authenticity_score,
            "enable_cultural_validation": self.enable_cultural_validation,
            "max_cultural_markers": self.max_cultural_markers,
            "enable_dialect_detection": self.enable_dialect_detection,
            "supported_languages": self.supported_languages,
            "enable_multilingual": self.enable_multilingual,
            "max_response_length": self.max_response_length,
            "enable_response_enhancement": self.enable_response_enhancement,
            "response_temperature": self.response_temperature,
            "max_concurrent_requests": self.max_concurrent_requests,
            "request_timeout": self.request_timeout,
            "enable_caching": self.enable_caching,
            "log_level": self.log_level,
            "enable_structured_logging": self.enable_structured_logging,
            "log_format": self.log_format,
            "default_variant": self.default_variant,
            "enable_variant_switching": self.enable_variant_switching,
            "variant_confidence_threshold": self.variant_confidence_threshold
        }
