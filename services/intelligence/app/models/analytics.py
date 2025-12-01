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
    issue_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    ticket_count = Column(Integer, default=0)
    estimated_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class SentimentMetric(Base):
    """Daily sentiment analysis metrics"""
    __tablename__ = "sentiment_metrics"

    id = Column(String, primary_key=True)  # UUID
    date = Column(Date, nullable=False, unique=True)
    average_score = Column(Float)  # 0.0 to 100.0
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class VolumeForecast(Base):
    """Ticket volume forecasts"""
    __tablename__ = "volume_forecasts"

    id = Column(String, primary_key=True)  # UUID
    date = Column(Date, nullable=False, unique=True)
    actual_volume = Column(Integer)  # NULL for future dates
    predicted_volume = Column(Integer, nullable=False)
    confidence_score = Column(Float)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


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
