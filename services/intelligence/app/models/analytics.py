"""
SQLAlchemy models for analytics and metrics.
"""
from sqlalchemy import Column, String, DateTime, Float, Integer, Date
from datetime import datetime
from app.core.database import Base


class RCAMetric(Base):
    """Root Cause Analysis metrics"""
    __tablename__ = "rca_metrics"

    id = Column(String, primary_key=True)  # UUID
    category = Column(String, nullable=False)  # e.g., "Shipping Delays"
    ticket_count = Column(Integer, default=0)
    avg_resolution_hours = Column(Float, default=0.0)
    severity = Column(String, nullable=False)  # "high", "medium", "low"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SentimentMetric(Base):
    """Daily sentiment analysis metrics"""
    __tablename__ = "sentiment_metrics"

    id = Column(String, primary_key=True)  # UUID
    date = Column(Date, nullable=False, unique=True)
    positive = Column(Integer, default=0)
    neutral = Column(Integer, default=0)
    negative = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VolumeForecast(Base):
    """Ticket volume forecasts"""
    __tablename__ = "volume_forecasts"

    id = Column(String, primary_key=True)  # UUID
    date = Column(Date, nullable=False, unique=True)
    actual = Column(Integer, nullable=True)  # NULL for future dates
    predicted = Column(Integer, nullable=False)
    lower_bound = Column(Integer, nullable=False)
    upper_bound = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AgentPerformance(Base):
    """Agent performance metrics"""
    __tablename__ = "agent_performance"

    id = Column(String, primary_key=True)  # UUID
    agent_name = Column(String, nullable=False)
    agent_email = Column(String)
    resolved_count = Column(Integer, default=0)
    average_resolution_time = Column(Float)  # hours
    csat_score = Column(Float)  # 1.0 to 5.0
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
