"""
Pydantic response models for API endpoints.
Ensures type safety and automatic validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    pending_approval = "pending_approval"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"
    critical = "critical"


class AIAnalysisResponse(BaseModel):
    sentiment: float = Field(..., ge=0, le=100, description="Sentiment score 0-100")
    intent: str = Field(..., description="Detected customer intent")
    priority_score: float = Field(..., ge=0, le=100)
    summary: str = Field(..., description="AI-generated summary")
    suggested_actions: Optional[List[str]] = None


class TicketResponse(BaseModel):
    id: str
    subject: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    source: str

class TicketListResponse(BaseModel):
    tickets: List[TicketResponse]
    total: int
    page: int
    page_size: int
    has_more: bool


class DashboardKPIs(BaseModel):
    open_tickets: int
    sla_risk_count: int
    avg_resolution_hours: float
    automation_rate: float
    total_tickets_7d: int
    resolved_tickets_7d: int


class TopicCluster(BaseModel):
    topic: str
    volume: int
    sentiment: float
    impact: str  # "Critical", "Medium", "Low"


class RegionalData(BaseModel):
    region: str
    volume: int
    sentiment: float
    friction_cost: float


class ChurnPrediction(BaseModel):
    customer: str
    customer_id: str
    ltv: float
    sentiment: float
    ticket_count: int
    churn_risk: str  # "High", "Medium", "Low"


class FrictionCostItem(BaseModel):
    category: str
    value: float
    type: str  # "positive", "negative", "result"


class StrategicRecommendation(BaseModel):
    id: str
    type: str  # "Logistics", "Product", "Policy"
    title: str
    description: str
    impact: str  # "High", "Critical", "Medium", "Low"
    confidence: str  # e.g., "94%"


class VolumeDataPoint(BaseModel):
    date: str
    actual: Optional[int] = None
    predicted: int
    lower_bound: Optional[int] = None
    upper_bound: Optional[int] = None


class SentimentTrendPoint(BaseModel):
    date: str
    score: float


class RCAItem(BaseModel):
    name: str
    count: int
    cost: Optional[float] = None
