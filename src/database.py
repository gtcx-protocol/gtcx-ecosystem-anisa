"""
ANISA Database Models and Configuration
PostgreSQL database for cultural intelligence persistence
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime, Text, Index, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.pool import NullPool
import os
import logging

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("ANISA_DB_URL", "postgresql://gtcx:gtcx@localhost:5432/gtcx")

# Create engine
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Use NullPool for better connection management
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class CulturalContext(Base):
    """Store analyzed cultural contexts"""
    __tablename__ = "anisa_cultural_contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    language = Column(String(10), nullable=False, default="en")
    region = Column(String(50), nullable=False, index=True)
    variant = Column(String(50), nullable=False, index=True)
    confidence_score = Column(Float, nullable=False)
    cultural_markers = Column(JSON, nullable=False, default=dict)
    trade_context = Column(String(100), index=True)
    
    # Relationships
    insights = relationship("CulturalInsight", back_populates="context")
    verifications = relationship("CulturalVerification", back_populates="context")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_region_variant', 'region', 'variant'),
        Index('idx_created_at', 'created_at'),
    )


class CulturalInsight(Base):
    """Store cultural insights and recommendations"""
    __tablename__ = "anisa_cultural_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    context_id = Column(Integer, ForeignKey('anisa_cultural_contexts.id'))
    event_type = Column(String(50), nullable=False, index=True)
    
    # Cultural analysis
    cultural_factors = Column(JSON, nullable=False, default=dict)
    compliance_factors = Column(JSON, default=dict)
    communication_style = Column(JSON, default=dict)
    decision_patterns = Column(JSON, default=dict)
    
    # Recommendations
    recommendations = Column(JSON, nullable=False, default=list)
    trade_implications = Column(JSON, default=dict)
    risk_factors = Column(JSON, default=list)
    
    # Scoring
    authenticity_score = Column(Float, nullable=False)
    relevance_score = Column(Float)
    
    # Relationship
    context = relationship("CulturalContext", back_populates="insights")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_event_type', 'event_type'),
        Index('idx_authenticity', 'authenticity_score'),
    )


class CulturalVerification(Base):
    """Track cultural verifications for PANX integration"""
    __tablename__ = "anisa_cultural_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    context_id = Column(Integer, ForeignKey('anisa_cultural_contexts.id'))
    
    # PANX integration
    panx_event_id = Column(String(100), index=True)
    lot_id = Column(String(100), index=True)
    validators = Column(JSON, default=list)
    
    # Cultural weights
    cultural_weights = Column(JSON, nullable=False, default=dict)
    consensus_adjustment = Column(Float, default=1.0)
    
    # Verification details
    verification_status = Column(String(20), default="pending")
    cultural_approval = Column(JSON, default=dict)
    community_feedback = Column(JSON, default=dict)
    
    # Relationship
    context = relationship("CulturalContext", back_populates="verifications")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    verified_at = Column(DateTime)
    
    # Indexes
    __table_args__ = (
        Index('idx_panx_event', 'panx_event_id'),
        Index('idx_lot_id', 'lot_id'),
    )


class CulturalKnowledge(Base):
    """Store cultural knowledge base entries"""
    __tablename__ = "anisa_cultural_knowledge"
    
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(50), nullable=False, index=True)
    variant = Column(String(50), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    
    # Knowledge content
    term = Column(String(200), nullable=False)
    definition = Column(Text)
    cultural_significance = Column(Text)
    trade_relevance = Column(Text)
    
    # Metadata
    source = Column(String(200))
    confidence_level = Column(Float, default=0.8)
    validated = Column(String(20), default="pending")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    validated_at = Column(DateTime)
    
    # Indexes
    __table_args__ = (
        Index('idx_region_variant_category', 'region', 'variant', 'category'),
        Index('idx_term', 'term'),
    )


class CulturalMetrics(Base):
    """Track ANISA performance metrics"""
    __tablename__ = "anisa_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Request metrics
    endpoint = Column(String(100), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    
    # Cultural metrics
    region = Column(String(50), index=True)
    variant = Column(String(50))
    authenticity_score = Column(Float)
    
    # Integration metrics
    panx_integrated = Column(String(5), default="false")
    cortex_forwarded = Column(String(5), default="false")
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_endpoint_timestamp', 'endpoint', 'timestamp'),
        Index('idx_metrics_timestamp', 'timestamp'),
    )


# Database helper functions
def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("ANISA database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_all_tables():
    """Drop all tables (use with caution)"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("All ANISA database tables dropped")
    except Exception as e:
        logger.error(f"Error dropping tables: {e}")
        raise
