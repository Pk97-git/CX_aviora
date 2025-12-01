"""
Strategy API routes.
Provides HQ-level strategic intelligence and analytics.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from typing import List
from datetime import datetime, timedelta

from app.api.models.responses import (
    TopicCluster,
    RegionalData,
    ChurnPrediction,
    FrictionCostItem,
    StrategicRecommendation
)
from app.core.database import get_db
from app.models.database import Ticket, AIAnalysis

router = APIRouter()


@router.get("/topics", response_model=List[TopicCluster])
async def get_topic_clusters(
    days: int = Query(30, ge=7, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Get semantic topic clusters (volume vs sentiment).
    
    Groups tickets by AI-detected intent and calculates:
    - Volume (ticket count)
    - Average sentiment
    - Impact level (Critical/Medium/Low)
    
    - **days**: Number of days to analyze (default: 30)
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = select(
        AIAnalysis.intent.label('topic'),
        func.count(AIAnalysis.id).label('volume'),
        func.avg(AIAnalysis.sentiment).label('sentiment'),
        case(
            (func.avg(AIAnalysis.sentiment) < 40, 'Critical'),
            (func.avg(AIAnalysis.sentiment) < 70, 'Medium'),
            else_='Low'
        ).label('impact')
    ).select_from(AIAnalysis).join(
        Ticket, AIAnalysis.ticket_id == Ticket.id
    ).where(
        Ticket.created_at >= start_date
    ).group_by(
        AIAnalysis.intent
    ).having(
        func.count(AIAnalysis.id) > 5  # Only show topics with >5 tickets
    ).order_by(
        func.count(AIAnalysis.id).desc()
    )
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        TopicCluster(
            topic=row.topic,
            volume=row.volume,
            sentiment=round(row.sentiment, 1),
            impact=row.impact
        )
        for row in rows
    ]


@router.get("/regional", response_model=List[RegionalData])
async def get_regional_intelligence(
    days: int = Query(30, ge=7, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Get regional intelligence (sentiment and friction cost by geography).
    
    - **days**: Number of days to analyze (default: 30)
    """
    from app.models.strategy import RegionalData as RegionalModel
    
    result = await db.execute(select(RegionalModel))
    regions = result.scalars().all()
    
    return [
        RegionalData(
            region=r.region,
            volume=r.ticket_volume,
            sentiment=round(r.avg_sentiment * 100, 1),  # Convert to 0-100 scale
            friction_cost=0.0  # Can be calculated from friction_costs table if needed
        )
        for r in regions
    ]


@router.get("/churn", response_model=List[ChurnPrediction])
async def get_churn_predictions(
    days: int = Query(90, ge=30, le=180),
    db: AsyncSession = Depends(get_db)
):
    """
    Get churn prediction for high-value customers.
    
    Identifies customers at risk based on:
    - Low sentiment scores
    - High ticket volume
    - Customer LTV
    
    - **days**: Number of days to analyze (default: 90)
    """
    from app.models.strategy import ChurnPrediction as ChurnModel
    
    result = await db.execute(select(ChurnModel).order_by(ChurnModel.risk_score.desc()))
    churn_data = result.scalars().all()
    
    return [
        ChurnPrediction(
            customer=c.customer_segment,
            customer_id=c.id[:8],  # Use first 8 chars of ID as customer_id
            ltv=float(c.affected_customers * 1000),  # Mock LTV calculation
            sentiment=round((1 - c.risk_score) * 100, 1),  # Inverse of risk
            ticket_count=c.affected_customers // 10,  # Mock ticket count
            churn_risk="High" if c.risk_score > 0.7 else "Medium" if c.risk_score > 0.4 else "Low"
        )
        for c in churn_data
    ]


@router.get("/friction-cost", response_model=List[FrictionCostItem])
async def get_friction_cost_analysis(
    days: int = Query(30, ge=7, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Get cost of friction analysis.
    
    Quantifies the dollar cost of bad CX experiences by category.
    
    - **days**: Number of days to analyze (default: 30)
    """
    from app.models.strategy import FrictionCost as FrictionModel
    
    result = await db.execute(
        select(FrictionModel).order_by(FrictionModel.estimated_cost.desc())
    )
    friction_items = result.scalars().all()
    
    # Calculate total potential revenue (sum of all costs)
    total_cost = sum(f.estimated_cost for f in friction_items)
    potential_revenue = total_cost * 1.5  # Assume 50% markup
    net_revenue = potential_revenue - total_cost
    
    # Build response with positive/negative values
    items = [
        FrictionCostItem(category="Potential Revenue", value=potential_revenue, type="positive")
    ]
    
    for f in friction_items:
        items.append(
            FrictionCostItem(
                category=f.friction_point,
                value=-f.estimated_cost,  # Negative for costs
                type="negative"
            )
        )
    
    items.append(
        FrictionCostItem(category="Net Revenue", value=net_revenue, type="result")
    )
    
    return items


@router.get("/recommendations", response_model=List[StrategicRecommendation])
async def get_strategic_recommendations(
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI-generated strategic recommendations.
    
    Top 3 moves to improve global CX and reduce revenue leakage.
    
    Note: In production, this would use ML models to generate
    recommendations based on current data patterns.
    """
    # Mock recommendations
    # In production, this would be generated by analyzing:
    # - Topic clusters with high volume + low sentiment
    # - Regional patterns
    # - Churn risk factors
    # - Historical resolution data
    
    recommendations = [
        {
            "id": 1,
            "type": "Logistics",
            "title": "Invest in EU Distribution Partner",
            "description": "Shipping delays in Europe are driving 40% of negative sentiment. A local partner could reduce friction cost by $3.2k/week.",
            "impact": "High",
            "confidence": "94%"
        },
        {
            "id": 2,
            "type": "Product",
            "title": "Fix 'Login Loop' Bug on iOS",
            "description": "Critical cluster 'App Crash' is correlated with the latest iOS update. 150 VIP customers affected.",
            "impact": "Critical",
            "confidence": "98%"
        },
        {
            "id": 3,
            "type": "Policy",
            "title": "Relax Return Policy for 'Sizing'",
            "description": "Sizing issues have neutral sentiment but high volume. Simplifying returns could boost LTV by 15%.",
            "impact": "Medium",
            "confidence": "85%"
        }
    ]
    
    return [StrategicRecommendation(**rec) for rec in recommendations]
