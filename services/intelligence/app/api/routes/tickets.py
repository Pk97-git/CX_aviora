"""
Ticket management API routes
"""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_tenant
from app.models.ticket import Ticket, TicketComment
from app.models.tenant import User, Tenant

router = APIRouter()


# Request/Response Models
class TicketResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    priority: Optional[str]
    customer_name: Optional[str]
    customer_email: Optional[str]
    assigned_to: Optional[str]
    assigned_team: Optional[str]
    ai_summary: Optional[str]
    ai_intent: Optional[str]
    ai_category: Optional[str]
    ai_sentiment: Optional[float]
    ai_priority: Optional[str]
    ai_suggested_actions: Optional[List[dict]]
    created_at: str
    updated_at: str


class TicketDetailResponse(TicketResponse):
    ai_entities: Optional[dict]
    tags: List[str]
    metadata: dict
    resolved_at: Optional[str]
    closed_at: Optional[str]


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_team: Optional[str] = None
    tags: Optional[List[str]] = None


class CommentCreate(BaseModel):
    content: str
    is_internal: bool = False


class CommentResponse(BaseModel):
    id: str
    author_name: Optional[str]
    author_type: str
    content: str
    is_internal: bool
    created_at: str


@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    assigned_to: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List tickets with filters"""
    query = select(Ticket).where(Ticket.tenant_id == tenant.id)
    
    if status:
        query = query.where(Ticket.status == status)
    if priority:
        query = query.where(Ticket.priority == priority)
    if category:
        query = query.where(Ticket.ai_category == category)
    if assigned_to:
        query = query.where(Ticket.assigned_to == assigned_to)
    if search:
        query = query.where(
            (Ticket.title.ilike(f"%{search}%")) |
            (Ticket.description.ilike(f"%{search}%"))
        )
    
    query = query.order_by(Ticket.created_at.desc()).limit(limit).offset(offset)
    
    result = await db.execute(query)
    tickets = result.scalars().all()
    
    return [
        TicketResponse(
            id=str(ticket.id),
            title=ticket.title,
            description=ticket.description,
            status=ticket.status,
            priority=ticket.priority,
            customer_name=ticket.customer_name,
            customer_email=ticket.customer_email,
            assigned_to=str(ticket.assigned_to) if ticket.assigned_to else None,
            assigned_team=ticket.assigned_team,
            ai_summary=ticket.ai_summary,
            ai_intent=ticket.ai_intent,
            ai_category=ticket.ai_category,
            ai_sentiment=ticket.ai_sentiment,
            ai_priority=ticket.ai_priority,
            ai_suggested_actions=ticket.ai_suggested_actions,
            created_at=ticket.created_at.isoformat(),
            updated_at=ticket.updated_at.isoformat() if ticket.updated_at else ticket.created_at.isoformat()
        )
        for ticket in tickets
    ]


@router.get("/{ticket_id}", response_model=TicketDetailResponse)
async def get_ticket(
    ticket_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get ticket details"""
    result = await db.execute(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.tenant_id == tenant.id
        )
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return TicketDetailResponse(
        id=str(ticket.id),
        title=ticket.title,
        description=ticket.description,
        status=ticket.status,
        priority=ticket.priority,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        assigned_to=str(ticket.assigned_to) if ticket.assigned_to else None,
        assigned_team=ticket.assigned_team,
        ai_summary=ticket.ai_summary,
        ai_intent=ticket.ai_intent,
        ai_category=ticket.ai_category,
        ai_sentiment=ticket.ai_sentiment,
        ai_priority=ticket.ai_priority,
        ai_suggested_actions=ticket.ai_suggested_actions,
        ai_entities=ticket.ai_entities,
        tags=ticket.tags or [],
        metadata=ticket.metadata or {},
        created_at=ticket.created_at.isoformat(),
        updated_at=ticket.updated_at.isoformat() if ticket.updated_at else ticket.created_at.isoformat(),
        resolved_at=ticket.resolved_at.isoformat() if ticket.resolved_at else None,
        closed_at=ticket.closed_at.isoformat() if ticket.closed_at else None
    )


@router.put("/{ticket_id}", response_model=TicketDetailResponse)
async def update_ticket(
    ticket_id: str,
    updates: TicketUpdate,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update ticket"""
    result = await db.execute(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.tenant_id == tenant.id
        )
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Update fields
    if updates.status is not None:
        ticket.status = updates.status
        if updates.status == 'resolved' and not ticket.resolved_at:
            ticket.resolved_at = datetime.utcnow()
        elif updates.status == 'closed' and not ticket.closed_at:
            ticket.closed_at = datetime.utcnow()
    
    if updates.priority is not None:
        ticket.priority = updates.priority
    if updates.assigned_to is not None:
        ticket.assigned_to = updates.assigned_to
    if updates.assigned_team is not None:
        ticket.assigned_team = updates.assigned_team
    if updates.tags is not None:
        ticket.tags = updates.tags
    
    ticket.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(ticket)
    
    return await get_ticket(ticket_id, tenant, user, db)


@router.get("/{ticket_id}/comments", response_model=List[CommentResponse])
async def list_comments(
    ticket_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List ticket comments"""
    result = await db.execute(
        select(TicketComment).where(
            TicketComment.ticket_id == ticket_id,
            TicketComment.tenant_id == tenant.id
        ).order_by(TicketComment.created_at.asc())
    )
    comments = result.scalars().all()
    
    return [
        CommentResponse(
            id=str(comment.id),
            author_name=comment.author_name,
            author_type=comment.author_type,
            content=comment.content,
            is_internal=comment.is_internal,
            created_at=comment.created_at.isoformat()
        )
        for comment in comments
    ]


@router.post("/{ticket_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    ticket_id: str,
    comment_data: CommentCreate,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add comment to ticket"""
    # Verify ticket exists
    result = await db.execute(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.tenant_id == tenant.id
        )
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    comment = TicketComment(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        ticket_id=ticket_id,
        author_type='user',
        author_id=user.id,
        author_name=user.full_name,
        author_email=user.email,
        content=comment_data.content,
        is_internal=comment_data.is_internal
    )
    
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    
    return CommentResponse(
        id=str(comment.id),
        author_name=comment.author_name,
        author_type=comment.author_type,
        content=comment.content,
        is_internal=comment.is_internal,
        created_at=comment.created_at.isoformat()
    )


@router.get("/stats/summary")
async def get_ticket_stats(
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get ticket statistics"""
    # Count by status
    status_result = await db.execute(
        select(
            Ticket.status,
            func.count(Ticket.id).label('count')
        ).where(
            Ticket.tenant_id == tenant.id
        ).group_by(Ticket.status)
    )
    status_counts = {row.status: row.count for row in status_result}
    
    # Count by priority
    priority_result = await db.execute(
        select(
            Ticket.priority,
            func.count(Ticket.id).label('count')
        ).where(
            Ticket.tenant_id == tenant.id
        ).group_by(Ticket.priority)
    )
    priority_counts = {row.priority: row.count for row in priority_result if row.priority}
    
    # Count by category
    category_result = await db.execute(
        select(
            Ticket.ai_category,
            func.count(Ticket.id).label('count')
        ).where(
            Ticket.tenant_id == tenant.id
        ).group_by(Ticket.ai_category)
    )
    category_counts = {row.ai_category: row.count for row in category_result if row.ai_category}
    
    return {
        "by_status": status_counts,
        "by_priority": priority_counts,
        "by_category": category_counts,
        "total": sum(status_counts.values())
    }
