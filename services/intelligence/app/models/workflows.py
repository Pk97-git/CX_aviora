"""
SQLAlchemy models for automation workflows.
"""
from sqlalchemy import Column, String, DateTime, Float, Integer, JSON, Text
from datetime import datetime
from app.core.database import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(String, primary_key=True)  # UUID
    name = Column(String, nullable=False)
    trigger_condition = Column(String)  # e.g., "Ticket Created > $500"
    actions = Column(JSON)  # List of actions to execute
    status = Column(String, nullable=False)  # active, paused
    total_runs = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    time_saved_hours = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
