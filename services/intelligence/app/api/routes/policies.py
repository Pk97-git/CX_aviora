from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.policies import Policy as PolicyModel

router = APIRouter()

class Policy(BaseModel):
    id: str
    name: str
    description: str
    status: str
    compliance_score: float
    violations_count: int
    last_updated: str

class PolicyStats(BaseModel):
    total_policies: int
    active_policies: int
    avg_compliance: float
    total_violations: int

@router.get("/", response_model=List[Policy])
async def get_policies(db: AsyncSession = Depends(get_db)):
    """Get all governance policies"""
    result = await db.execute(select(PolicyModel))
    policies = result.scalars().all()
    
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "status": p.status,
            "compliance_score": p.compliance_score,
            "violations_count": p.violations_count,
            "last_updated": p.last_updated.strftime("%Y-%m-%d") if p.last_updated else ""
        }
        for p in policies
    ]

@router.get("/policies/stats", response_model=PolicyStats)
async def get_policy_stats(db: AsyncSession = Depends(get_db)):
    """Get policy compliance statistics"""
    # Get total count
    total_result = await db.execute(select(func.count(PolicyModel.id)))
    total = total_result.scalar()
    
    # Get active count
    active_result = await db.execute(
        select(func.count(PolicyModel.id)).where(PolicyModel.status == "active")
    )
    active = active_result.scalar()
    
    # Get average compliance
    avg_result = await db.execute(select(func.avg(PolicyModel.compliance_score)))
    avg_compliance = avg_result.scalar() or 0.0
    
    # Get total violations
    violations_result = await db.execute(select(func.sum(PolicyModel.violations_count)))
    total_violations = violations_result.scalar() or 0
    
    return {
        "total_policies": total,
        "active_policies": active,
        "avg_compliance": round(avg_compliance / 100, 2),  # Convert to 0-1 scale
        "total_violations": total_violations
    }
