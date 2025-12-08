"""
SQLAlchemy models for strategic intelligence.
"""
from sqlalchemy import Column, String, DateTime, Float, Integer, JSON
from datetime import datetime
from app.core.database import Base


class TopicCluster(Base):
    """Semantic topic clustering"""
    __tablename__ = "topic_clusters"

    id = Column(String, primary_key=True)  # UUID
    topic = Column(String, nullable=False, unique=True)
    volume = Column(Integer, default=0)
    trend = Column(String)  # rising, stable, falling
    keywords = Column(JSON)  # List of keywords
    avg_sentiment = Column(Float)  # -1.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RegionalData(Base):
    """Regional intelligence metrics"""
    __tablename__ = "regional_data"

    id = Column(String, primary_key=True)  # UUID
    region = Column(String, nullable=False, unique=True)
    country_code = Column(String)  # ISO country code
    ticket_volume = Column(Integer, default=0)
    avg_sentiment = Column(Float)  # -1.0 to 1.0
    top_issues = Column(JSON)  # List of top issues
    resolution_rate = Column(Float)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChurnPrediction(Base):
    """Customer churn predictions"""
    __tablename__ = "churn_predictions"

    id = Column(String, primary_key=True)  # UUID
    customer_segment = Column(String, nullable=False)
    risk_score = Column(Float, nullable=False)  # 0.0 to 1.0
    affected_customers = Column(Integer, default=0)
    risk_factors = Column(JSON)  # List of contributing factors
    recommended_actions = Column(JSON)  # List of recommended actions
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FrictionCost(Base):
    """Cost of friction analysis"""
    __tablename__ = "friction_costs"

    id = Column(String, primary_key=True)  # UUID
    friction_point = Column(String, nullable=False)
    category = Column(String)  # e.g., "Payment", "Shipping", "Login"
    estimated_cost = Column(Float, default=0.0)
    ticket_count = Column(Integer, default=0)
    impact_score = Column(Float)  # 0.0 to 10.0
    resolution_difficulty = Column(String)  # easy, medium, hard
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StrategicRecommendation(Base):
    """AI-generated strategic recommendations"""
    __tablename__ = "strategic_recommendations"

    id = Column(String, primary_key=True)  # UUID
    type = Column(String, nullable=False)  # Logistics, Product, Policy, etc.
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    impact = Column(String, nullable=False)  # High, Critical, Medium, Low
    confidence = Column(String, nullable=False)  # e.g. "94%"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
