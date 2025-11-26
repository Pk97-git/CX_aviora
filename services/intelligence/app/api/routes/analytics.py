"""
Analytics API routes.
Provides dashboard KPIs and insights data.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.models.responses import (
    DashboardKPIs,
    RCAItem,
    SentimentTrendPoint,
    VolumeDataPoint
)
from app.api.db import get_dashboard_kpis, get_rca_data, get_sentiment_trend
from app.core.database import get_db
from app.core.cache import redis_cache

router = APIRouter()


@router.get("/summary", response_model=DashboardKPIs)
@redis_cache(prefix="analytics:summary", ttl=60)  # 1-minute cache
async def get_summary(db: AsyncSession = Depends(get_db)):
    """
    Get dashboard summary KPIs for the last 7 days.
    
    Returns:
    - Open tickets count
    - SLA risk count
    - Average resolution time (hours)
    - Automation rate
    - Total tickets (7 days)
    - Resolved tickets (7 days)
    """
    kpis = await get_dashboard_kpis(db)
    return DashboardKPIs(**kpis)


@router.get("/rca", response_model=List[RCAItem])
@redis_cache(prefix="analytics:rca", ttl=300)  # 5-minute cache
async def get_root_cause_analysis(
    days: int = Query(30, ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Get Root Cause Analysis - top issues by volume.
    
    - **days**: Number of days to analyze (default: 30, max: 90)
    """
    rca_data = await get_rca_data(db, days=days)
    return [RCAItem(**item) for item in rca_data]


@router.get("/sentiment", response_model=List[SentimentTrendPoint])
@redis_cache(prefix="analytics:sentiment", ttl=300)  # 5-minute cache
async def get_sentiment_analysis(
    days: int = Query(7, ge=1, le=30),
    db: AsyncSession = Depends(get_db)
):
    """
    Get sentiment trend over time.
    
    - **days**: Number of days to analyze (default: 7, max: 30)
    """
    sentiment_data = await get_sentiment_trend(db, days=days)
    return [SentimentTrendPoint(**item) for item in sentiment_data]


@router.get("/volume-forecast", response_model=List[VolumeDataPoint])
async def get_volume_forecast(
    days: int = Query(30, ge=7, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Get 30-day volume forecast with confidence intervals.
    
    - **days**: Number of days to forecast (default: 30, max: 90)
    
    Note: This is a simplified forecast. Production would use time-series ML models.
    """
    from datetime import datetime, timedelta
    from app.models.database import Ticket
    from sqlalchemy import select, func
    
    # Get historical average for baseline
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    query = select(
        func.count(Ticket.id)
    ).where(
        Ticket.created_at >= seven_days_ago
    )
    
    result = await db.execute(query)
    total_7d = result.scalar() or 0
    avg_daily = total_7d / 7
    
    # Generate forecast (simplified linear projection with noise)
    forecast = []
    for i in range(days):
        day_offset = i + 1
        date_str = f"Day {day_offset}"
        
        # Simple forecast with slight growth trend
        predicted = int(avg_daily * (1 + (day_offset * 0.01)))
        
        # Confidence intervals (±20%)
        lower = int(predicted * 0.8)
        upper = int(predicted * 1.2)
        
        # Only include actual data for past days (mock)
        actual = int(avg_daily) if i < 5 else None
        
        forecast.append(VolumeDataPoint(
            date=date_str,
            actual=actual,
            predicted=predicted,
            lower_bound=lower,
            upper_bound=upper
        ))
    
    return forecast
