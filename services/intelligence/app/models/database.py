"""
SQLAlchemy Base class for all models.
All model definitions are in their respective domain files:
- tenant.py: Tenant, User, APIKey, Integration
- ticket.py: Ticket, TicketComment
- analytics.py, executive.py, strategy.py, etc.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
