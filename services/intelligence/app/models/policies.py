"""
SQLAlchemy models for policies and governance.
"""
from sqlalchemy import Column, String, DateTime, Float, Integer, JSON, Text
from datetime import datetime
from app.core.database import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(String, primary_key=True)  # UUID
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False)  # active, monitoring, paused
    compliance_score = Column(Float)  # 0.0 to 100.0
    rule_definition = Column(JSON)  # Policy rules in JSON format
    violations_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
