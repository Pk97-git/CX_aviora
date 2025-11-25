from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class TicketEvent(BaseModel):
    ticket_id: str
    title: str
    description: str
    source: str
    created_at: Optional[str] = None

class AnalysisResult(BaseModel):
    sentiment: str
    intent: str
    urgency_score: int
    category: str
    summary: str
