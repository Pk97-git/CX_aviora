from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Policy(BaseModel):
    id: int
    name: str
    category: str
    description: str
    status: str
    compliance_score: float
    violations: int
    last_updated: str

class PolicyStats(BaseModel):
    total_policies: int
    active_policies: int
    avg_compliance: float
    total_violations: int

@router.get("/policies", response_model=List[Policy])
async def get_policies():
    """Get all governance policies"""
    return [
        {
            "id": 1,
            "name": "Response Time SLA",
            "category": "Performance",
            "description": "All tickets must receive first response within 2 hours during business hours",
            "status": "active",
            "compliance_score": 0.94,
            "violations": 23,
            "last_updated": "2024-11-15"
        },
        {
            "id": 2,
            "name": "VIP Customer Priority",
            "category": "Customer Tier",
            "description": "VIP customers must be assigned to senior agents within 15 minutes",
            "status": "active",
            "compliance_score": 0.98,
            "violations": 5,
            "last_updated": "2024-11-20"
        },
        {
            "id": 3,
            "name": "Refund Approval Workflow",
            "category": "Financial",
            "description": "Refunds over $500 require manager approval before processing",
            "status": "active",
            "compliance_score": 1.0,
            "violations": 0,
            "last_updated": "2024-11-10"
        },
        {
            "id": 4,
            "name": "Data Privacy Compliance",
            "category": "Security",
            "description": "Customer PII must not be shared in public channels or external tools",
            "status": "active",
            "compliance_score": 0.96,
            "violations": 12,
            "last_updated": "2024-11-18"
        },
        {
            "id": 5,
            "name": "Escalation Protocol",
            "category": "Process",
            "description": "Tickets with negative sentiment below 30% must be escalated to management",
            "status": "active",
            "compliance_score": 0.89,
            "violations": 34,
            "last_updated": "2024-11-12"
        }
    ]

@router.get("/policies/stats", response_model=PolicyStats)
async def get_policy_stats():
    """Get policy compliance statistics"""
    return {
        "total_policies": 5,
        "active_policies": 5,
        "avg_compliance": 0.95,
        "total_violations": 74
    }
