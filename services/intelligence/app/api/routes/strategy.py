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
    
    Note: This is a simplified version. Production would use actual
    geographic data from customer records.
    
    - **days**: Number of days to analyze (default: 30)
    """
    # Mock regional data for now
    # In production, this would query customer.region or ticket.region
    mock_regions = [
        {"region": "North America", "volume": 1200, "sentiment": 78.0, "friction_cost": 4500.0},
        {"region": "Europe", "sentiment": 65.0, "volume": 850, "friction_cost": 3200.0},
        {"region": "Asia Pacific", "volume": 600, "sentiment": 82.0, "friction_cost": 1800.0},
        {"region": "LATAM", "volume": 300, "sentiment": 70.0, "friction_cost": 900.0},
    ]
    
    return [RegionalData(**region) for region in mock_regions]


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
    # Note: This requires a customers table with LTV data
    # For now, returning mock data
    # In production, this would be a complex query joining tickets, customers, and analysis
    
    mock_churn_data = [
        {
            "customer": "Acme Corp",
            "customer_id": "cust_001",
            "ltv": 45000.0,
            "sentiment": 25.0,
            "ticket_count": 12,
            "churn_risk": "High"
        },
        {
            "customer": "TechStart Inc",
            "customer_id": "cust_002",
            "ltv": 32000.0,
            "sentiment": 40.0,
            "ticket_count": 8,
            "churn_risk": "High"
        },
        {
            "customer": "Global Retail",
            "customer_id": "cust_003",
            "ltv": 28000.0,
            "sentiment": 55.0,
            "ticket_count": 5,
            "churn_risk": "Medium"
        },
        {
            "customer": "FastShip Co",
            "customer_id": "cust_004",
            "ltv": 18000.0,
            "sentiment": 70.0,
            "ticket_count": 3,
            "churn_risk": "Low"
        },
        {
            "customer": "CloudBase",
            "customer_id": "cust_005",
            "ltv": 52000.0,
            "sentiment": 80.0,
            "ticket_count": 2,
            "churn_risk": "Low"
        },
        {
            "customer": "DataFlow Ltd",
            "customer_id": "cust_006",
            "ltv": 15000.0,
            "sentiment": 35.0,
            "ticket_count": 10,
            "churn_risk": "High"
        },
    ]
    
    return [ChurnPrediction(**item) for item in mock_churn_data]


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
    # Mock friction cost data
    # In production, this would calculate based on:
    # - Ticket volume by category
    # - Average cost per ticket type
    # - Lost revenue estimates
    
    friction_data = [
        {"category": "Potential Revenue", "value": 125000.0, "type": "positive"},
        {"category": "Shipping Delays", "value": -12000.0, "type": "negative"},
        {"category": "Login Issues", "value": -8500.0, "type": "negative"},
        {"category": "Sizing Returns", "value": -6200.0, "type": "negative"},
        {"category": "App Crashes", "value": -4300.0, "type": "negative"},
        {"category": "Net Revenue", "value": 94000.0, "type": "result"},
    ]
    
    return [FrictionCostItem(**item) for item in friction_data]


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
