"""
Webhook receivers for external ticketing systems
"""
from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime
from typing import Optional
import logging

from app.core.database import get_db
from app.models.ticket import Ticket
from app.models.tenant import Tenant
from app.services.ticket_understanding import TicketUnderstandingService
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


async def get_tenant_from_webhook(
    x_tenant_id: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> Tenant:
    """Extract tenant from webhook headers"""
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing X-Tenant-ID header")
    
    result = await db.execute(
        select(Tenant).where(Tenant.id == x_tenant_id)
    )
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return tenant


def map_freshdesk_status(status: int) -> str:
    """Map Freshdesk status codes to our status"""
    status_map = {
        2: 'open',
        3: 'pending',
        4: 'resolved',
        5: 'closed',
    }
    return status_map.get(status, 'open')


def map_freshdesk_priority(priority: int) -> str:
    """Map Freshdesk priority codes to our priority"""
    priority_map = {
        1: 'low',
        2: 'medium',
        3: 'high',
        4: 'urgent',
    }
    return priority_map.get(priority, 'medium')


@router.post("/freshdesk")
async def freshdesk_webhook(
    request: Request,
    tenant: Tenant = Depends(get_tenant_from_webhook),
    db: AsyncSession = Depends(get_db)
):
    """
    Receive webhooks from Freshdesk
    
    Headers required:
    - X-Tenant-ID: Your tenant UUID
    """
    try:
        payload = await request.json()
        logger.info(f"Received Freshdesk webhook for tenant {tenant.id}")
        
        # Freshdesk sends ticket data in different formats depending on event
        ticket_data = payload.get("freshdesk_webhook", payload)
        
        # Check if ticket already exists
        external_id = str(ticket_data.get("id"))
        result = await db.execute(
            select(Ticket).where(
                Ticket.tenant_id == tenant.id,
                Ticket.source == "freshdesk",
                Ticket.external_id == external_id
            )
        )
        existing_ticket = result.scalar_one_or_none()
        
        if existing_ticket:
            # Update existing ticket
            existing_ticket.title = ticket_data.get("subject", existing_ticket.title)
            existing_ticket.description = ticket_data.get("description_text", existing_ticket.description)
            existing_ticket.status = map_freshdesk_status(ticket_data.get("status", 2))
            existing_ticket.priority = map_freshdesk_priority(ticket_data.get("priority", 2))
            existing_ticket.updated_at = datetime.utcnow()
            
            await db.commit()
            return {"status": "updated", "ticket_id": str(existing_ticket.id)}
        
        # Create new ticket
        ticket = Ticket(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            external_id=external_id,
            source="freshdesk",
            title=ticket_data.get("subject", "No subject"),
            description=ticket_data.get("description_text", ""),
            status=map_freshdesk_status(ticket_data.get("status", 2)),
            priority=map_freshdesk_priority(ticket_data.get("priority", 2)),
            customer_email=ticket_data.get("requester", {}).get("email"),
            customer_name=ticket_data.get("requester", {}).get("name"),
        )
        
        # Run AI analysis
        ai_service = TicketUnderstandingService(settings.GROQ_API_KEY)
        analysis = await ai_service.analyze_ticket(
            ticket.title,
            ticket.description
        )
        
        # Update ticket with AI insights
        ticket.ai_summary = analysis.summary
        ticket.ai_intent = analysis.intent
        ticket.ai_entities = analysis.entities
        ticket.ai_sentiment = analysis.sentiment
        ticket.ai_priority = analysis.priority
        ticket.ai_category = analysis.category
        ticket.ai_suggested_actions = analysis.suggested_actions
        
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        
        logger.info(f"Created ticket {ticket.id} from Freshdesk")
        
        return {
            "status": "created",
            "ticket_id": str(ticket.id),
            "ai_analysis": {
                "intent": analysis.intent,
                "category": analysis.category,
                "sentiment": analysis.sentiment
            }
        }
        
    except Exception as e:
        logger.error(f"Freshdesk webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zendesk")
async def zendesk_webhook(
    request: Request,
    tenant: Tenant = Depends(get_tenant_from_webhook),
    db: AsyncSession = Depends(get_db)
):
    """
    Receive webhooks from Zendesk
    
    Headers required:
    - X-Tenant-ID: Your tenant UUID
    """
    try:
        payload = await request.json()
        logger.info(f"Received Zendesk webhook for tenant {tenant.id}")
        
        ticket_data = payload.get("ticket", payload)
        
        # Create ticket
        ticket = Ticket(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            external_id=str(ticket_data.get("id")),
            source="zendesk",
            title=ticket_data.get("subject", "No subject"),
            description=ticket_data.get("description", ""),
            status=ticket_data.get("status", "open"),
            priority=ticket_data.get("priority", "normal"),
            customer_email=ticket_data.get("requester", {}).get("email"),
            customer_name=ticket_data.get("requester", {}).get("name"),
        )
        
        # Run AI analysis
        ai_service = TicketUnderstandingService(settings.GROQ_API_KEY)
        analysis = await ai_service.analyze_ticket(
            ticket.title,
            ticket.description
        )
        
        ticket.ai_summary = analysis.summary
        ticket.ai_intent = analysis.intent
        ticket.ai_entities = analysis.entities
        ticket.ai_sentiment = analysis.sentiment
        ticket.ai_priority = analysis.priority
        ticket.ai_category = analysis.category
        ticket.ai_suggested_actions = analysis.suggested_actions
        
        db.add(ticket)
        await db.commit()
        
        return {"status": "created", "ticket_id": str(ticket.id)}
        
    except Exception as e:
        logger.error(f"Zendesk webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/manual")
async def create_manual_ticket(
    request: Request,
    tenant: Tenant = Depends(get_tenant_from_webhook),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a ticket manually via API
    
    Headers required:
    - X-Tenant-ID: Your tenant UUID
    
    Body:
    {
      "title": "Ticket title",
      "description": "Ticket description",
      "customer_email": "customer@example.com",
      "customer_name": "John Doe"
    }
    """
    try:
        data = await request.json()
        
        ticket = Ticket(
            id=uuid.uuid4(),
            tenant_id=tenant.id,
            source="manual",
            title=data.get("title", "No title"),
            description=data.get("description", ""),
            customer_email=data.get("customer_email"),
            customer_name=data.get("customer_name"),
            status="open",
            priority="medium"
        )
        
        # Run AI analysis
        ai_service = TicketUnderstandingService(settings.GROQ_API_KEY)
        analysis = await ai_service.analyze_ticket(
            ticket.title,
            ticket.description
        )
        
        ticket.ai_summary = analysis.summary
        ticket.ai_intent = analysis.intent
        ticket.ai_entities = analysis.entities
        ticket.ai_sentiment = analysis.sentiment
        ticket.ai_priority = analysis.priority
        ticket.ai_category = analysis.category
        ticket.ai_suggested_actions = analysis.suggested_actions
        
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        
        return {
            "status": "created",
            "ticket_id": str(ticket.id),
            "ai_analysis": {
                "summary": analysis.summary,
                "intent": analysis.intent,
                "category": analysis.category,
                "sentiment": analysis.sentiment,
                "suggested_priority": analysis.priority
            }
        }
        
    except Exception as e:
        logger.error(f"Manual ticket creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
