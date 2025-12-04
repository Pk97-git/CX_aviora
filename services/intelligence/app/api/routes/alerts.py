"""
Alerts API routes for real-time notifications.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from uuid import uuid4

from app.core.database import get_db
from app.models.executive import Alert, AlertRule
from app.models.ticket import Ticket
from app.models.strategy import ChurnPrediction
from app.models.analytics import SentimentMetric

router = APIRouter()


# Request/Response Models
class AlertRuleCreate(BaseModel):
    name: str
    metric_type: str  # 'sla_breach', 'churn_risk', 'sentiment_drop', 'volume_spike'
    threshold_value: float
    severity: str  # 'critical', 'high', 'medium', 'low'
    notification_channels: List[str]  # ['email', 'slack', 'webhook']


class AlertRuleResponse(BaseModel):
    id: str
    name: str
    metric_type: str
    threshold_value: float
    severity: str
    notification_channels: List[str]
    enabled: bool
    created_at: datetime


class AlertResponse(BaseModel):
    id: str
    alert_type: str
    severity: str
    title: str
    message: str
    metric_value: Optional[float]
    triggered_at: datetime
    acknowledged_at: Optional[datetime]
    acknowledged_by: Optional[str]


class AcknowledgeRequest(BaseModel):
    acknowledged_by: str


@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    active_only: bool = True,
    severity: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get recent alerts.
    
    - **active_only**: Only return unacknowledged alerts (default: true)
    - **severity**: Filter by severity level
    - **limit**: Maximum number of alerts to return (default: 50)
    """
    query = select(Alert).order_by(Alert.triggered_at.desc())
    
    if active_only:
        query = query.where(Alert.acknowledged_at.is_(None))
    
    if severity:
        query = query.where(Alert.severity == severity)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    
    return [
        AlertResponse(
            id=a.id,
            alert_type=a.alert_type,
            severity=a.severity,
            title=a.title,
            message=a.message,
            metric_value=a.metric_value,
            triggered_at=a.triggered_at,
            acknowledged_at=a.acknowledged_at,
            acknowledged_by=a.acknowledged_by
        )
        for a in alerts
    ]


@router.get("/active", response_model=List[AlertResponse])
async def get_active_alerts(db: AsyncSession = Depends(get_db)):
    """Get all unacknowledged alerts."""
    result = await db.execute(
        select(Alert)
        .where(Alert.acknowledged_at.is_(None))
        .order_by(Alert.triggered_at.desc())
    )
    alerts = result.scalars().all()
    
    return [
        AlertResponse(
            id=a.id,
            alert_type=a.alert_type,
            severity=a.severity,
            title=a.title,
            message=a.message,
            metric_value=a.metric_value,
            triggered_at=a.triggered_at,
            acknowledged_at=a.acknowledged_at,
            acknowledged_by=a.acknowledged_by
        )
        for a in alerts
    ]


@router.put("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    request: AcknowledgeRequest,
    db: AsyncSession = Depends(get_db)
):
    """Acknowledge an alert."""
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id)
    )
    alert = result.scalar_one_or_none()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.acknowledged_at = datetime.utcnow()
    alert.acknowledged_by = request.acknowledged_by
    
    await db.commit()
    
    return {"status": "acknowledged", "alert_id": alert_id}


@router.get("/rules", response_model=List[AlertRuleResponse])
async def get_alert_rules(
    enabled_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Get all alert rules."""
    query = select(AlertRule)
    
    if enabled_only:
        query = query.where(AlertRule.enabled == True)
    
    result = await db.execute(query)
    rules = result.scalars().all()
    
    return [
        AlertRuleResponse(
            id=r.id,
            name=r.name,
            metric_type=r.metric_type,
            threshold_value=r.threshold_value,
            severity=r.severity,
            notification_channels=r.notification_channels,
            enabled=r.enabled,
            created_at=r.created_at
        )
        for r in rules
    ]


@router.post("/rules", response_model=AlertRuleResponse)
async def create_alert_rule(
    rule: AlertRuleCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new alert rule."""
    new_rule = AlertRule(
        id=str(uuid4()),
        name=rule.name,
        metric_type=rule.metric_type,
        threshold_value=rule.threshold_value,
        severity=rule.severity,
        notification_channels=rule.notification_channels,
        enabled=True,
        created_at=datetime.utcnow()
    )
    
    db.add(new_rule)
    await db.commit()
    await db.refresh(new_rule)
    
    return AlertRuleResponse(
        id=new_rule.id,
        name=new_rule.name,
        metric_type=new_rule.metric_type,
        threshold_value=new_rule.threshold_value,
        severity=new_rule.severity,
        notification_channels=new_rule.notification_channels,
        enabled=new_rule.enabled,
        created_at=new_rule.created_at
    )


@router.post("/check")
async def check_alerts(db: AsyncSession = Depends(get_db)):
    """
    Check all alert rules and generate alerts if thresholds are exceeded.
    This endpoint would typically be called by a scheduled job.
    """
    # Get all enabled alert rules
    result = await db.execute(
        select(AlertRule).where(AlertRule.enabled == True)
    )
    rules = result.scalars().all()
    
    alerts_generated = []
    
    for rule in rules:
        alert = await _check_rule(rule, db)
        if alert:
            alerts_generated.append(alert)
    
    return {
        "status": "checked",
        "rules_checked": len(rules),
        "alerts_generated": len(alerts_generated),
        "alerts": alerts_generated
    }


async def _check_rule(rule: AlertRule, db: AsyncSession) -> Optional[dict]:
    """Check a single alert rule and generate alert if needed."""
    
    if rule.metric_type == "sla_breach":
        # Check for SLA risk tickets
        result = await db.execute(
            select(func.count(Ticket.id))
            .where(
                and_(
                    Ticket.status.in_(['open', 'in_progress']),
                    Ticket.sla_due_at < datetime.utcnow()
                )
            )
        )
        count = result.scalar() or 0
        
        if count > rule.threshold_value:
            alert = Alert(
                id=str(uuid4()),
                rule_id=rule.id,
                alert_type="sla_breach",
                severity=rule.severity,
                title=f"SLA Breach Alert: {count} tickets at risk",
                message=f"{count} tickets have breached or are about to breach SLA. Immediate action required.",
                metric_value=float(count),
                triggered_at=datetime.utcnow()
            )
            db.add(alert)
            await db.commit()
            return {"type": "sla_breach", "count": count}
    
    elif rule.metric_type == "churn_risk":
        # Check for high churn risk customers
        result = await db.execute(
            select(func.count(ChurnPrediction.id))
            .where(ChurnPrediction.risk_score >= 0.7)  # High risk threshold
        )
        count = result.scalar() or 0
        
        if count > rule.threshold_value:
            alert = Alert(
                id=str(uuid4()),
                rule_id=rule.id,
                alert_type="churn_risk",
                severity=rule.severity,
                title=f"High Churn Risk: {count} customers",
                message=f"{count} customers are at high risk of churning. Review and take preventive action.",
                metric_value=float(count),
                triggered_at=datetime.utcnow()
            )
            db.add(alert)
            await db.commit()
            return {"type": "churn_risk", "count": count}
    
    elif rule.metric_type == "sentiment_drop":
        # Check for sentiment drop
        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)
        
        # Get recent sentiment
        recent_result = await db.execute(
            select(func.avg(SentimentMetric.positive))
            .where(SentimentMetric.date >= week_ago)
        )
        recent_avg = recent_result.scalar() or 0
        
        # Get previous week sentiment
        two_weeks_ago = week_ago - timedelta(days=7)
        previous_result = await db.execute(
            select(func.avg(SentimentMetric.positive))
            .where(
                and_(
                    SentimentMetric.date >= two_weeks_ago,
                    SentimentMetric.date < week_ago
                )
            )
        )
        previous_avg = previous_result.scalar() or 0
        
        if previous_avg > 0:
            drop_percentage = ((recent_avg - previous_avg) / previous_avg) * 100
            
            if drop_percentage < rule.threshold_value:  # Negative threshold
                alert = Alert(
                    id=str(uuid4()),
                    rule_id=rule.id,
                    alert_type="sentiment_drop",
                    severity=rule.severity,
                    title=f"Sentiment Drop Alert: {abs(drop_percentage):.1f}% decrease",
                    message=f"Customer sentiment has dropped by {abs(drop_percentage):.1f}% in the past week. Investigate root causes.",
                    metric_value=drop_percentage,
                    triggered_at=datetime.utcnow()
                )
                db.add(alert)
                await db.commit()
                return {"type": "sentiment_drop", "drop_percentage": drop_percentage}
    
    elif rule.metric_type == "volume_spike":
        # Check for ticket volume spike
        today = datetime.utcnow()
        result = await db.execute(
            select(func.count(Ticket.id))
            .where(
                func.date(Ticket.created_at) == today.date()
            )
        )
        count = result.scalar() or 0
        
        if count > rule.threshold_value:
            alert = Alert(
                id=str(uuid4()),
                rule_id=rule.id,
                alert_type="volume_spike",
                severity=rule.severity,
                title=f"Volume Spike: {count} tickets today",
                message=f"Ticket volume has spiked to {count} today. Consider increasing support capacity.",
                metric_value=float(count),
                triggered_at=datetime.utcnow()
            )
            db.add(alert)
            await db.commit()
            return {"type": "volume_spike", "count": count}
    
    return None
