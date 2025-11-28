"""
Tickets API routes.
Handles ticket CRUD operations with AI analysis.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.api.models.responses import (
    TicketResponse,
    TicketListResponse,
    TicketStatus,
    TicketPriority
)
from app.api.db import get_tickets_with_analysis
from app.core.database import get_db
from app.models.database import Ticket

router = APIRouter()


@router.get("", response_model=TicketListResponse)
async def list_tickets(
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    List tickets with optional filters and pagination.
    
    - **status**: Filter by ticket status
    - **priority**: Filter by priority level
    - **start_date**: Filter tickets created after this date
    - **end_date**: Filter tickets created before this date
    - **page**: Page number (1-indexed)
    - **page_size**: Number of items per page (max 100)
    """
    offset = (page - 1) * page_size
    
    tickets, total = await get_tickets_with_analysis(
        db=db,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        start_date=start_date,
        end_date=end_date,
        limit=page_size,
        offset=offset
    )
    
    has_more = (offset + len(tickets)) < total
    
    return TicketListResponse(
        tickets=tickets,
        total=total,
        page=page,
        page_size=page_size,
        has_more=has_more
    )


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single ticket by ID with AI analysis.
    """
    from sqlalchemy import select
    from app.models.database import AIAnalysis
    
    # Fetch ticket with analysis
    query = select(Ticket, AIAnalysis).outerjoin(
        AIAnalysis, Ticket.id == AIAnalysis.ticket_id
    ).where(Ticket.id == ticket_id)
    
    if not row:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket, analysis = row
    
    # MAP DB FIELDS TO FRONTEND EXPECTATIONS
    ticket_dict = {
        "id": ticket.id,
        "subject": ticket.title,  # DB: title -> Frontend: subject
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "source": ticket.external_source,  # DB: external_source -> Frontend: source
        "customer_id": ticket.customer_id,
        "customer_email": ticket.customer_email,
        "assignee": ticket.assigned_to,  # DB: assigned_to -> Frontend: assignee
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
    
    return TicketResponse(**ticket_dict)


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str,
    status: Optional[TicketStatus] = None,
    assignee: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Update ticket status or assignee.
    """
    from sqlalchemy import select, update
    
    # Check if ticket exists
    query = select(Ticket).where(Ticket.id == ticket_id)
    result = await db.execute(query)
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Build update dict
    update_data = {"updated_at": datetime.utcnow()}
    
    if status:
        update_data["status"] = status.value
        if status == TicketStatus.resolved:
            update_data["resolved_at"] = datetime.utcnow()
    
    if assignee is not None:
        update_data["assignee"] = assignee
    
    # Update ticket
    update_query = (
        update(Ticket)
        .where(Ticket.id == ticket_id)
        .values(**update_data)
    )
    await db.execute(update_query)
    await db.commit()
    
    # Return updated ticket
    return await get_ticket(ticket_id, db)
