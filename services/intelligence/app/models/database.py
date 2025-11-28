"""
SQLAlchemy database models for tickets and AI analysis.
"""
from sqlalchemy import Column, String, DateTime, Integer, Float, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True)  # UUID in DB but SQLAlchemy can handle as String
    tenant_id = Column(String)
    external_id = Column(String)
    external_source = Column(String)
    title = Column(String, nullable=False)  # Changed from 'subject'
    description = Column(Text)
    status = Column(String, nullable=False, default="open")
    priority = Column(String, default="medium")
    category = Column(String)
    subcategory = Column(String)
    intent = Column(String)
    sentiment = Column(String)
    urgency_score = Column(Float)
    entities = Column(JSON)
    assigned_to = Column(String)
    customer_id = Column(String)
    customer_email = Column(String)
    customer_name = Column(String)
    sla_due_at = Column(DateTime)
    sla_breached = Column(Integer)  # Boolean in DB
    tags = Column(JSON)  # ARRAY in DB
    ticket_metadata = Column("metadata", JSON)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)
    closed_at = Column(DateTime)


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(String, primary_key=True)  # UUID in DB
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)
    sentiment = Column(Float)
    intent = Column(String)
    urgency = Column(String)
    category = Column(String)
    priority_score = Column(Float)
    summary = Column(Text)
    suggested_actions = Column(JSON)  # JSONB in DB
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
