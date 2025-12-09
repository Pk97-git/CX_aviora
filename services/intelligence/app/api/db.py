"""
Database utility functions for API routes.
"""
from sqlalchemy import select, func, and_, or_, case
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


async def get_tickets_with_analysis(
    db: AsyncSession,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0
) -> tuple[List[Dict[str, Any]], int]:
    """
    Fetch tickets with AI analysis, with optional filters.
    Returns (tickets, total_count)
    """
    from app.models.ticket import Ticket, AIAnalysis
    
    # Build query
    query = select(Ticket, AIAnalysis).outerjoin(
        AIAnalysis, Ticket.id == AIAnalysis.ticket_id
    )
    
    # Apply filters
    filters = []
    if status:
        filters.append(Ticket.status == status)
    if priority:
        filters.append(Ticket.priority == priority)
    if start_date:
        filters.append(Ticket.created_at >= start_date)
    if end_date:
        filters.append(Ticket.created_at <= end_date)
    
    if filters:
        query = query.where(and_(*filters))
    
    # Get total count
    count_query = select(func.count()).select_from(Ticket)
    if filters:
        count_query = count_query.where(and_(*filters))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination and ordering
    query = query.order_by(Ticket.created_at.desc()).limit(limit).offset(offset)
    
    result = await db.execute(query)
    rows = result.all()
    
    # Format results - MAP DB FIELDS TO FRONTEND EXPECTATIONS + Convert UUIDs to strings
    tickets = []
    for ticket, analysis in rows:
        # MAP DB FIELDS TO FRONTEND EXPECTATIONS + Convert UUIDs to strings
        ticket_dict = {
            "id": str(ticket.id),  # UUID -> str
            "subject": ticket.title,  # DB: title -> Frontend: subject
            "description": ticket.description or "",
            "status": ticket.status,
            "priority": ticket.priority,
            "source": ticket.external_source or "",  # DB: external_source -> Frontend: source
            "customer_id": str(ticket.customer_id) if ticket.customer_id else None,  # UUID -> str
            "customer_email": ticket.customer_email or "",
            "customer_name": ticket.customer_name or "",
            "assignee": str(ticket.assigned_to) if ticket.assigned_to else None,  # DB: assigned_to -> Frontend: assignee, UUID -> str
            "created_at": ticket.created_at,
            "updated_at": ticket.updated_at,
            "resolved_at": ticket.resolved_at,
            "sla_breach_at": ticket.sla_due_at,  # DB: sla_due_at -> Frontend: sla_breach_at
        }
        
        if analysis:
            ticket_dict["ai_analysis"] = {
                "sentiment": analysis.sentiment,
                "intent": analysis.intent,
                "priority_score": analysis.priority_score,
                "summary": analysis.summary,
                "suggested_actions": analysis.suggested_actions or []
            }
        
        tickets.append(ticket_dict)
    
    return tickets, total


async def get_dashboard_kpis(db: AsyncSession) -> Dict[str, Any]:
    """
    Calculate dashboard KPIs for the last 7 days.
    """
    from app.models.ticket import Ticket
    
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Open tickets
    open_count_query = select(func.count()).select_from(Ticket).where(
        Ticket.status == 'open'
    )
    open_result = await db.execute(open_count_query)
    open_tickets = open_result.scalar() or 0
    
    # SLA risk (urgent/critical tickets with approaching SLA)
    sla_risk_query = select(func.count()).select_from(Ticket).where(
        and_(
            Ticket.priority.in_(['urgent', 'critical']),
            Ticket.sla_due_at < datetime.utcnow() + timedelta(hours=2),
            Ticket.status.in_(['open', 'in_progress'])
        )
    )
    sla_risk_result = await db.execute(sla_risk_query)
    sla_risk = sla_risk_result.scalar() or 0
    
    # Average resolution time (in hours)
    avg_resolution_query = select(
        func.avg(
            func.extract('epoch', Ticket.resolved_at - Ticket.created_at) / 3600
        )
    ).select_from(Ticket).where(
        and_(
            Ticket.resolved_at.isnot(None),
            Ticket.created_at >= seven_days_ago
        )
    )
    avg_result = await db.execute(avg_resolution_query)
    avg_resolution = avg_result.scalar() or 0.0
    
    # Total tickets in last 7 days
    total_7d_query = select(func.count()).select_from(Ticket).where(
        Ticket.created_at >= seven_days_ago
    )
    total_7d_result = await db.execute(total_7d_query)
    total_7d = total_7d_result.scalar() or 0
    
    # Resolved tickets in last 7 days
    resolved_7d_query = select(func.count()).select_from(Ticket).where(
        and_(
            Ticket.resolved_at.isnot(None),
            Ticket.created_at >= seven_days_ago
        )
    )
    resolved_7d_result = await db.execute(resolved_7d_query)
    resolved_7d = resolved_7d_result.scalar() or 0
    
    # Automation rate (placeholder - would need automation tracking)
    automation_rate = 62.0  # Mock for now
    
    return {
        "open_tickets": open_tickets,
        "sla_risk_count": sla_risk,
        "avg_resolution_hours": round(avg_resolution, 1),
        "automation_rate": automation_rate,
        "total_tickets_7d": total_7d,
        "resolved_tickets_7d": resolved_7d
    }


async def get_rca_data(db: AsyncSession, days: int = 30) -> List[Dict[str, Any]]:
    """
    Get Root Cause Analysis - top issues by volume.
    """
    from app.models.ticket import Ticket, AIAnalysis
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = select(
        AIAnalysis.intent.label('name'),
        func.count(AIAnalysis.id).label('count'),
        func.avg(AIAnalysis.sentiment).label('avg_sentiment')
    ).select_from(AIAnalysis).join(
        Ticket, AIAnalysis.ticket_id == Ticket.id
    ).where(
        Ticket.created_at >= start_date
    ).group_by(
        AIAnalysis.intent
    ).order_by(
        func.count(AIAnalysis.id).desc()
    ).limit(10)
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        {
            "name": row.name,
            "count": row.count,
            "cost": row.count * 15  # Mock cost calculation
        }
        for row in rows
    ]


async def get_sentiment_trend(db: AsyncSession, days: int = 7) -> List[Dict[str, Any]]:
    """
    Get sentiment trend over the last N days.
    """
    from app.models.ticket import Ticket, AIAnalysis
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = select(
        func.date(Ticket.created_at).label('date'),
        func.avg(AIAnalysis.sentiment).label('score')
    ).select_from(AIAnalysis).join(
        Ticket, AIAnalysis.ticket_id == Ticket.id
    ).where(
        Ticket.created_at >= start_date
    ).group_by(
        func.date(Ticket.created_at)
    ).order_by(
        func.date(Ticket.created_at)
    )
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        {
            "date": row.date.strftime('%a'),
            "score": round(row.score, 1)
        }
        for row in rows
    ]
