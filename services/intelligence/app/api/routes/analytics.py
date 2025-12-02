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
    from app.models.analytics import RCAMetric
    from sqlalchemy import select
    
    result = await db.execute(
        select(RCAMetric).order_by(RCAMetric.ticket_count.desc()).limit(10)
    )
    metrics = result.scalars().all()
    
    return [
        RCAItem(
            name=m.category,
            count=m.ticket_count,
            cost=int(m.avg_resolution_hours * m.ticket_count * 50)  # $50/hour estimate
        )
        for m in metrics
    ]


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
    from app.models.analytics import SentimentMetric
    from sqlalchemy import select
    from datetime import datetime, timedelta
    
    start_date = datetime.utcnow().date() - timedelta(days=days)
    
    result = await db.execute(
        select(SentimentMetric)
        .where(SentimentMetric.date >= start_date)
        .order_by(SentimentMetric.date)
    )
    metrics = result.scalars().all()
    
    return [
        SentimentTrendPoint(
            date=m.date.strftime('%a'),
            positive=m.positive,
            neutral=m.neutral,
            negative=m.negative
        )
        for m in metrics
    ]


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
    from app.models.analytics import VolumeForecast
    from sqlalchemy import select
    from datetime import datetime, timedelta
    
    start_date = datetime.utcnow().date()
    end_date = start_date + timedelta(days=days)
    
    result = await db.execute(
        select(VolumeForecast)
        .where(VolumeForecast.date >= start_date)
        .where(VolumeForecast.date < end_date)
        .order_by(VolumeForecast.date)
        .limit(days)
    )
    forecasts = result.scalars().all()
    
    return [
        VolumeDataPoint(
            date=f.date.strftime('%b %d'),
            actual=f.actual,
            predicted=f.predicted,
            lower_bound=f.lower_bound,
            upper_bound=f.upper_bound
        )
        for f in forecasts
    ]
