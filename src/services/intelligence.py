"""
Intelligence Service
"""

import logging
import random
from typing import List, Dict, Any
from ..models import CulturalContext, NativeUnderstanding, IntelligentResponse, CulturalVariant
from ..config import ANISAConfig


class IntelligenceService:
    """Service for generating culturally intelligent responses."""
    
    def __init__(self, config: ANISAConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Response templates for each cultural variant
        self.response_templates = {
            CulturalVariant.UBUNTU: {
                "greeting": [
                    "Greetings! I'm here to help you in the spirit of ubuntu - together we are stronger.",
                    "Welcome! In our community, we believe that 'I am because we are.' How can I assist you?",
                    "Hello! Let us work together, for the village raises the child. What do you need?"
                ],
                "problem_solving": [
                    "Let us think about this together. In our community, we find solutions through collective wisdom.",
                    "This challenge affects us all. Let me help you find a way that benefits everyone.",
                    "Together we can overcome this. What have you tried so far?"
                ],
                "advice": [
                    "Consider how this decision will impact our community. We are all connected.",
                    "Think of the elders' wisdom: every action ripples through the village.",
                    "Remember, what helps one helps all. Let's find the best path forward."
                ]
            },
            CulturalVariant.JUGAAD: {
                "greeting": [
                    "Namaste! I'm here to help you find creative solutions - that's the jugaad way!",
                    "Hello! Let's think outside the box and find innovative ways to solve your challenges.",
                    "Greetings! In jugaad, we believe there's always a creative way to make things work."
                ],
                "problem_solving": [
                    "Let's approach this with jugaad thinking - creative, resourceful, and practical.",
                    "Constraints often lead to the most innovative solutions. What resources do you have?",
                    "Think creatively! Sometimes the best solution is the simplest one that works."
                ],
                "advice": [
                    "Be resourceful with what you have. Jugaad teaches us to optimize and innovate.",
                    "Don't let limitations stop you - they can inspire your most creative solutions.",
                    "Focus on what works, not what's perfect. Practical solutions win the day."
                ]
            },
            CulturalVariant.GUANXI: {
                "greeting": [
                    "你好! I'm here to help you build the right connections and relationships.",
                    "Greetings! In guanxi, we understand the importance of building trust and connections.",
                    "Hello! Let me help you navigate this through the power of relationships."
                ],
                "problem_solving": [
                    "Let's think about who might help us with this. Relationships are key to solutions.",
                    "In guanxi, we solve problems by building the right connections. Who do you know?",
                    "Trust and relationships open doors. Let's find the right people to help."
                ],
                "advice": [
                    "Build relationships first, solutions will follow. Guanxi is about long-term connections.",
                    "Consider how this affects your network. Maintain face and honor in all dealings.",
                    "Invest in relationships now, they will help you in the future."
                ]
            },
            CulturalVariant.JEITINHO: {
                "greeting": [
                    "Olá! I'm here to help you find flexible and creative solutions - that's jeitinho!",
                    "Hello! Let me help you find a smart way around this challenge.",
                    "Greetings! In jeitinho, we believe there's always a creative workaround."
                ],
                "problem_solving": [
                    "Let's find a jeitinho - a smart, flexible solution that works for you.",
                    "Sometimes the best solution is the most creative one. What's your situation?",
                    "Be flexible and creative. Jeitinho is about finding smart ways to make things work."
                ],
                "advice": [
                    "Think flexibly about this. Sometimes the unconventional path is the best one.",
                    "Don't be rigid - adapt to the situation. That's the jeitinho way.",
                    "Find your own path. Jeitinho is about personal, creative solutions."
                ]
            },
            CulturalVariant.WASTA: {
                "greeting": [
                    "مرحبا! I'm here to help you through connections and influence - that's wasta!",
                    "Hello! Let me help you navigate this using the right connections.",
                    "Greetings! In wasta, we understand the power of networks and influence."
                ],
                "problem_solving": [
                    "Let's think about who can help us. Wasta is about using connections wisely.",
                    "Your network is your strength. Who do you know who can assist?",
                    "Influence and connections open doors. Let's find the right approach."
                ],
                "advice": [
                    "Build your network carefully. Wasta is about reciprocal relationships.",
                    "Use your influence to help others, and they will help you in return.",
                    "Maintain your connections. They are valuable assets in solving problems."
                ]
            }
        }
        
        # Cultural markers for responses
        self.cultural_markers = {
            CulturalVariant.UBUNTU: ["community", "together", "village", "harmony", "respect", "unity"],
            CulturalVariant.JUGAAD: ["creative", "innovative", "resourceful", "solution", "smart", "clever"],
            CulturalVariant.GUANXI: ["relationship", "connection", "trust", "honor", "network", "face"],
            CulturalVariant.JEITINHO: ["flexible", "creative", "smart", "solution", "workaround", "adaptable"],
            CulturalVariant.WASTA: ["connection", "influence", "network", "help", "support", "relationship"]
        }
        
        self.logger.info("Intelligence Service initialized")
    
    async def generate_cultural_response(
        self, 
        user_input: str, 
        cultural_context: CulturalContext, 
        native_understanding: NativeUnderstanding
    ) -> IntelligentResponse:
        """Generate a culturally intelligent response."""
        try:
            # Determine response type based on input
            response_type = self._determine_response_type(user_input, native_understanding)
            
            # Generate response text
            response_text = self._generate_response_text(
                response_type, cultural_context, native_understanding
            )
            
            # Calculate authenticity score
            authenticity_score = self._calculate_authenticity_score(
                response_text, cultural_context, native_understanding
            )
            
            # Extract cultural markers used
            markers_used = self._extract_cultural_markers_used(response_text, cultural_context.variant)
            
            # Create response metadata
            metadata = {
                "response_type": response_type,
                "generation_method": "template_based",
                "enhancement_applied": True
            }
            
            return IntelligentResponse(
                response_text=response_text,
                cultural_variant=cultural_context.variant,
                authenticity_score=authenticity_score,
                cultural_markers_used=markers_used,
                response_metadata=metadata
            )
            
        except Exception as e:
            self.logger.error(f"Error generating cultural response: {e}")
            return self._create_error_response(cultural_context, str(e))
    
    def _determine_response_type(self, user_input: str, understanding) -> str:
        """Determine the type of response needed."""
        input_lower = user_input.lower()
        
        # Check for specific patterns
        if any(word in input_lower for word in ["hello", "hi", "greetings", "good morning"]):
            return "greeting"
        
        if any(word in input_lower for word in ["help", "problem", "issue", "trouble", "difficulty"]):
            return "problem_solving"
        
        if any(word in input_lower for word in ["advice", "suggest", "recommend", "what should"]):
            return "advice"
        
        # Default based on sentiment
        if hasattr(understanding, 'contextual_meaning') and understanding.contextual_meaning.get("sentiment") == "negative":
            return "advice"
        else:
            return "problem_solving"
    
    def _generate_response_text(self, response_type: str, context: CulturalContext, understanding) -> str:
        """Generate response text based on type and cultural context."""
        variant = context.variant
        
        if variant in self.response_templates and response_type in self.response_templates[variant]:
            templates = self.response_templates[variant][response_type]
            base_response = random.choice(templates)
        else:
            # Fallback response
            base_response = f"I understand you need help. Let me assist you in a way that respects your {variant.value} cultural background."
        
        # Enhance response with cultural insights
        enhanced_response = self._enhance_with_cultural_insights(base_response, understanding, context)
        
        # Ensure response length is within limits
        if len(enhanced_response) > self.config.max_response_length:
            enhanced_response = enhanced_response[:self.config.max_response_length - 3] + "..."
        
        return enhanced_response
    
    def _enhance_with_cultural_insights(self, base_response: str, understanding, context: CulturalContext) -> str:
        """Enhance response with cultural insights and understanding."""
        enhanced = base_response
        
        # Add cultural insights if available
        if hasattr(understanding, 'cultural_insights') and understanding.cultural_insights:
            insight = random.choice(understanding.cultural_insights)
            if "Community" in insight:
                enhanced += " Remember, we're stronger together."
            elif "Creative" in insight:
                enhanced += " Your creativity will find the way."
            elif "Relationship" in insight:
                enhanced += " Building connections is key."
        
        return enhanced
    
    def _calculate_authenticity_score(self, response_text: str, context: CulturalContext, understanding) -> float:
        """Calculate the cultural authenticity score of the response."""
        base_score = 0.8  # Base score for template-based responses
        
        # Boost score based on cultural marker usage
        markers_used = self._extract_cultural_markers_used(response_text, context.variant)
        marker_score = min(0.2, len(markers_used) * 0.05)
        
        # Boost score based on cultural insights integration
        insight_score = 0.0
        if hasattr(understanding, 'cultural_insights') and understanding.cultural_insights:
            insight_score = min(0.1, len(understanding.cultural_insights) * 0.02)
        
        total_score = base_score + marker_score + insight_score
        
        return min(1.0, total_score)
    
    def _extract_cultural_markers_used(self, response_text: str, variant: CulturalVariant) -> List[str]:
        """Extract cultural markers used in the response."""
        markers = []
        text_lower = response_text.lower()
        
        if variant in self.cultural_markers:
            for marker in self.cultural_markers[variant]:
                if marker in text_lower:
                    markers.append(marker)
        
        return markers
    
    def _create_error_response(self, context: CulturalContext, error_message: str) -> IntelligentResponse:
        """Create an error response when generation fails."""
        error_text = f"I apologize, but I encountered an issue: {error_message}. Please try again."
        
        return IntelligentResponse(
            response_text=error_text,
            cultural_variant=context.variant,
            authenticity_score=0.5,  # Low score for error responses
            cultural_markers_used=["error_response"],
            response_metadata={"is_error": True, "error": error_message}
        )
