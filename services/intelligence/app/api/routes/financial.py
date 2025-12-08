"""
Financial metrics and executive dashboard API routes.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, timedelta, date
from pydantic import BaseModel
from decimal import Decimal

from app.core.database import get_db
from app.models.executive import FinancialMetric, ROICalculation

router = APIRouter()


# Response Models
class FinancialImpactSummary(BaseModel):
    total_value_generated: float
    revenue_protected: float
    cost_saved: float
    churn_prevented_count: int
    automation_cost_saved: float  # Changed from automation_savings
    friction_cost_reduced: float  # Changed from friction_reduction
    resolution_time_saved_hours: float  # Added missing field
    sla_compliance_bonus: float  # Added missing field
    period_start: str
    period_end: str


class ROIResponse(BaseModel):
    roi_percentage: float
    total_investment: float
    total_return: float
    period_start: str
    period_end: str
    breakdown: dict


class FinancialTrendPoint(BaseModel):
    date: str
    value_generated: float
    revenue_protected: float
    cost_saved: float


@router.get("/impact", response_model=FinancialImpactSummary)
async def get_financial_impact(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """
    Get financial impact summary for the specified period.
    
    - **days**: Number of days to analyze (default: 30, max: 365)
    
    Returns aggregated financial metrics including revenue protected,
    cost savings, and total value generated.
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # Query financial metrics for the period
    result = await db.execute(
        select(
            func.sum(FinancialMetric.total_value_generated).label('total_value'),
            func.sum(FinancialMetric.revenue_protected).label('revenue'),
            func.sum(FinancialMetric.automation_cost_saved).label('automation'),
            func.sum(FinancialMetric.friction_cost_reduced).label('friction'),
            func.sum(FinancialMetric.churn_prevented_count).label('churn_count')
        ).where(
            FinancialMetric.date >= start_date,
            FinancialMetric.date <= end_date
        )
    )
    
    row = result.first()
    
    total_value = float(row.total_value or 0)
    revenue = float(row.revenue or 0)
    automation = float(row.automation or 0)
    friction = float(row.friction or 0)
    cost_saved = automation + friction
    
    # Query for time saved and SLA bonus
    time_result = await db.execute(
        select(
            func.sum(FinancialMetric.resolution_time_saved_hours).label('time_saved'),
            func.sum(FinancialMetric.sla_compliance_bonus).label('sla_bonus')
        ).where(
            FinancialMetric.date >= start_date,
            FinancialMetric.date <= end_date
        )
    )
    time_row = time_result.first()
    
    return FinancialImpactSummary(
        total_value_generated=total_value,
        revenue_protected=revenue,
        cost_saved=cost_saved,
        churn_prevented_count=row.churn_count or 0,
        automation_cost_saved=automation,  # Changed field name
        friction_cost_reduced=friction,  # Changed field name
        resolution_time_saved_hours=float(time_row.time_saved or 0),  # Added
        sla_compliance_bonus=float(time_row.sla_bonus or 0),  # Added
        period_start=start_date.isoformat(),
        period_end=end_date.isoformat()
    )


@router.get("/roi", response_model=ROIResponse)
async def get_roi(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """
    Calculate ROI for the specified period.
    
    - **days**: Number of days to analyze (default: 30, max: 365)
    
    Returns ROI percentage, total investment, and total return.
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # Check if we have a pre-calculated ROI for this period
    result = await db.execute(
        select(ROICalculation)
        .where(
            ROICalculation.period_start == start_date,
            ROICalculation.period_end == end_date
        )
        .order_by(ROICalculation.calculated_at.desc())
        .limit(1)
    )
    
    roi_calc = result.scalar_one_or_none()
    
    if roi_calc:
        return ROIResponse(
            roi_percentage=roi_calc.roi_percentage,
            total_investment=float(roi_calc.total_investment),
            total_return=float(roi_calc.total_return),
            period_start=roi_calc.period_start.isoformat(),
            period_end=roi_calc.period_end.isoformat(),
            breakdown=roi_calc.breakdown or {}
        )
    
    # Calculate ROI on the fly if not pre-calculated
    impact_result = await db.execute(
        select(
            func.sum(FinancialMetric.total_value_generated).label('total_return')
        ).where(
            FinancialMetric.date >= start_date,
            FinancialMetric.date <= end_date
        )
    )
    
    total_return = float(impact_result.scalar() or 0)
    
    # Estimate investment (simplified - would be more complex in production)
    # Assume $10k/month for platform costs
    months = days / 30
    total_investment = 10000 * months
    
    roi_percentage = ((total_return - total_investment) / total_investment * 100) if total_investment > 0 else 0
    
    return ROIResponse(
        roi_percentage=round(roi_percentage, 2),
        total_investment=total_investment,
        total_return=total_return,
        period_start=start_date.isoformat(),
        period_end=end_date.isoformat(),
        breakdown={
            "automation_savings": 0,  # Would calculate from data
            "churn_prevention": 0,
            "friction_reduction": 0
        }
    )


@router.get("/trends", response_model=List[FinancialTrendPoint])
async def get_financial_trends(
    days: int = Query(30, ge=7, le=365),
    db: AsyncSession = Depends(get_db)
):
    """
    Get financial trends over time.
    
    - **days**: Number of days to analyze (default: 30, max: 365)
    
    Returns daily financial metrics for trend visualization.
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    result = await db.execute(
        select(FinancialMetric)
        .where(
            FinancialMetric.date >= start_date,
            FinancialMetric.date <= end_date
        )
        .order_by(FinancialMetric.date)
    )
    
    metrics = result.scalars().all()
    
    return [
        FinancialTrendPoint(
            date=m.date.strftime('%b %d'),
            value_generated=float(m.total_value_generated),
            revenue_protected=float(m.revenue_protected),
            cost_saved=float(m.automation_cost_saved + m.friction_cost_reduced)
        )
        for m in metrics
    ]


@router.get("/breakdown")
async def get_financial_breakdown(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed breakdown of financial impact by category.
    
    - **days**: Number of days to analyze (default: 30, max: 365)
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    result = await db.execute(
        select(
            func.sum(FinancialMetric.revenue_protected).label('revenue_protected'),
            func.sum(FinancialMetric.automation_cost_saved).label('automation_savings'),
            func.sum(FinancialMetric.friction_cost_reduced).label('friction_reduction'),
            func.sum(FinancialMetric.sla_compliance_bonus).label('sla_bonus'),
            func.sum(FinancialMetric.resolution_time_saved_hours).label('time_saved')
        ).where(
            FinancialMetric.date >= start_date,
            FinancialMetric.date <= end_date
        )
    )
    
    row = result.first()
    
    return {
        "categories": [
            {
                "name": "Churn Prevention",
                "value": float(row.revenue_protected or 0),
                "description": "Revenue protected by preventing customer churn"
            },
            {
                "name": "Automation Savings",
                "value": float(row.automation_savings or 0),
                "description": "Cost saved through workflow automation"
            },
            {
                "name": "Friction Reduction",
                "value": float(row.friction_reduction or 0),
                "description": "Value from reducing customer friction points"
            },
            {
                "name": "SLA Compliance",
                "value": float(row.sla_bonus or 0),
                "description": "Bonus from meeting SLA targets"
            }
        ],
        "time_saved_hours": float(row.time_saved or 0),
        "period_start": start_date.isoformat(),
        "period_end": end_date.isoformat()
    }
