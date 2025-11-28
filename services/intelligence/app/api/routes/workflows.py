from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Workflow(BaseModel):
    id: int
    name: str
    trigger: str
    actions: List[str]
    status: str
    success_rate: float
    time_saved_hours: int
    executions: int

class WorkflowStats(BaseModel):
    total_workflows: int
    active_workflows: int
    total_executions: int
    time_saved_hours: int
    avg_success_rate: float

@router.get("/workflows", response_model=List[Workflow])
async def get_workflows():
    """Get all automation workflows"""
    return [
        {
            "id": 1,
            "name": "Auto-assign to Billing Team",
            "trigger": "Intent: Billing",
            "actions": ["Assign to Billing", "Add 'billing' tag", "Set priority: High"],
            "status": "active",
            "success_rate": 0.94,
            "time_saved_hours": 120,
            "executions": 1250
        },
        {
            "id": 2,
            "name": "Escalate VIP Negative Sentiment",
            "trigger": "Customer: VIP + Sentiment < 40%",
            "actions": ["Notify manager", "Assign to senior agent", "Set priority: Urgent"],
            "status": "active",
            "success_rate": 0.98,
            "time_saved_hours": 85,
            "executions": 340
        },
        {
            "id": 3,
            "name": "Auto-close Resolved Tickets",
            "trigger": "Status: Pending Approval + 48h no response",
            "actions": ["Send satisfaction survey", "Close ticket", "Archive"],
            "status": "active",
            "success_rate": 0.89,
            "time_saved_hours": 200,
            "executions": 2100
        },
        {
            "id": 4,
            "name": "Route Shipping Delays",
            "trigger": "Topic: Shipping Delay",
            "actions": ["Assign to Logistics", "Add tracking info template", "Set SLA: 4h"],
            "status": "paused",
            "success_rate": 0.92,
            "time_saved_hours": 65,
            "executions": 890
        }
    ]

@router.get("/workflows/stats", response_model=WorkflowStats)
async def get_workflow_stats():
    """Get workflow statistics"""
    return {
        "total_workflows": 4,
        "active_workflows": 3,
        "total_executions": 4580,
        "time_saved_hours": 470,
        "avg_success_rate": 0.93
    }
