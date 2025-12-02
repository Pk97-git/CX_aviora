from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.workflows import Workflow as WorkflowModel

router = APIRouter()

class Workflow(BaseModel):
    id: str
    name: str
    trigger: str
    actions: List[str]
    status: str
    success_rate: float
    time_saved_hours: float
    executions: int

class WorkflowStats(BaseModel):
    total_workflows: int
    active_workflows: int
    total_executions: int
    time_saved_hours: float
    avg_success_rate: float

@router.get("/", response_model=List[Workflow])
async def get_workflows(db: AsyncSession = Depends(get_db)):
    """Get all automation workflows"""
    result = await db.execute(select(WorkflowModel))
    workflows = result.scalars().all()
    
    return [
        {
            "id": w.id,
            "name": w.name,
            "trigger": w.trigger_condition,
            "actions": w.actions,  # Already JSON
            "status": w.status,
            "success_rate": round(w.success_count / w.total_runs, 2) if w.total_runs > 0 else 0.0,
            "time_saved_hours": w.time_saved_hours,
            "executions": w.total_runs
        }
        for w in workflows
    ]

@router.get("/stats", response_model=WorkflowStats)
async def get_workflow_stats(db: AsyncSession = Depends(get_db)):
    """Get workflow statistics"""
    # Get total count
    total_result = await db.execute(select(func.count(WorkflowModel.id)))
    total = total_result.scalar()
    
    # Get active count
    active_result = await db.execute(
        select(func.count(WorkflowModel.id)).where(WorkflowModel.status == "active")
    )
    active = active_result.scalar()
    
    # Get total executions
    executions_result = await db.execute(select(func.sum(WorkflowModel.total_runs)))
    total_executions = executions_result.scalar() or 0
    
    # Get total time saved
    time_result = await db.execute(select(func.sum(WorkflowModel.time_saved_hours)))
    time_saved = time_result.scalar() or 0.0
    
    # Get average success rate
    result = await db.execute(select(WorkflowModel))
    workflows = result.scalars().all()
    avg_success = sum(w.success_count / w.total_runs if w.total_runs > 0 else 0 for w in workflows) / len(workflows) if workflows else 0.0
    
    return {
        "total_workflows": total,
        "active_workflows": active,
        "total_executions": total_executions,
        "time_saved_hours": time_saved,
        "avg_success_rate": round(avg_success, 2)
    }
