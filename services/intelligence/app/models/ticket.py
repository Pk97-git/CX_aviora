"""
Ticket and related models for ticket management system
"""
from sqlalchemy import Column, String, Text, Float, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.models.database import Base


class Ticket(Base):
    """Customer support ticket"""
    __tablename__ = "tickets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Source Information
    external_id = Column(String(255))
    source = Column(String(50), nullable=False)  # 'freshdesk', 'zendesk', 'intercom', 'manual'
    
    # Basic Fields
    title = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='open')  # 'open', 'pending', 'resolved', 'closed'
    priority = Column(String(20))  # 'low', 'medium', 'high', 'urgent'
    
    # Customer Information
    customer_email = Column(String(255))
    customer_name = Column(String(255))
    customer_id = Column(String(255))
    
    # Assignment
    assigned_to = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    assigned_team = Column(String(100))  # 'support', 'engineering', 'finance'
    
    # AI-Generated Fields
    ai_summary = Column(Text)
    ai_intent = Column(String(100))  # 'refund_request', 'bug_report', 'feature_request', etc.
    ai_entities = Column(JSONB)  # {"order_id": "12345", "amount": 99.99}
    ai_sentiment = Column(Float)  # -1.0 to 1.0
    ai_priority = Column(String(20))  # AI-suggested priority
    ai_suggested_actions = Column(JSONB)  # [{"action": "refund", "confidence": 0.95}]
    ai_category = Column(String(100))  # 'billing', 'technical', 'account', etc.
    
    # Metadata
    tags = Column(JSONB, default=[])
    ticket_metadata = Column("metadata", JSONB, default={})  # Use column name override to avoid reserved word
    
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)
    closed_at = Column(DateTime)
    
    # Relationships
    tenant = relationship("Tenant")
    assigned_user = relationship("User", foreign_keys=[assigned_to])
    comments = relationship("TicketComment", back_populates="ticket", cascade="all, delete-orphan")


class TicketComment(Base):
    """Comments/replies on tickets"""
    __tablename__ = "ticket_comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False, index=True)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey('tickets.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Author Information
    author_type = Column(String(20))  # 'user', 'customer', 'system'
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    author_name = Column(String(255))
    author_email = Column(String(255))
    
    # Content
    content = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)  # Internal notes vs customer-visible
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    ticket = relationship("Ticket", back_populates="comments")
    author = relationship("User", foreign_keys=[author_id])


# Pydantic model for AI analysis results (used by services)
from pydantic import BaseModel
from typing import List, Dict, Optional

class AnalysisResult(BaseModel):
    """AI analysis results for a ticket"""
    summary: str
    intent: str
    category: str
    sentiment: float
    urgency_score: Optional[float] = None
    entities: Optional[Dict] = None
    suggested_actions: Optional[List[Dict]] = None
