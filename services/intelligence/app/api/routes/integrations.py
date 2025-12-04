"""
Integration management API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Dict

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_tenant, require_role
from app.models.tenant import User, Tenant, Integration
from app.integrations.freshdesk import FreshdeskIntegration
from app.integrations.jira import JiraIntegration
from app.integrations.slack import SlackIntegration

router = APIRouter()


# Request/Response Models
class TestConnectionResponse(BaseModel):
    status: str
    message: str
    details: Dict = {}


class CreateJiraIssueRequest(BaseModel):
    ticket_id: str


class SendSlackNotificationRequest(BaseModel):
    ticket_id: str


@router.post("/integrations/{integration_id}/test", response_model=TestConnectionResponse)
async def test_integration(
    integration_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Test integration connection"""
    # Get integration
    result = await db.execute(
        select(Integration).where(
            Integration.id == integration_id,
            Integration.tenant_id == tenant.id
        )
    )
    integration = result.scalar_one_or_none()
    
    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    # Test based on type
    try:
        if integration.type == 'freshdesk':
            client = FreshdeskIntegration(integration.config)
            result = await client.test_connection()
        elif integration.type == 'jira':
            client = JiraIntegration(integration.config)
            result = await client.test_connection()
        elif integration.type == 'slack':
            client = SlackIntegration(integration.config)
            result = await client.test_connection()
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported integration type: {integration.type}")
        
        return TestConnectionResponse(
            status=result.get('status', 'error'),
            message=result.get('message', 'Unknown error'),
            details=result
        )
    except Exception as e:
        return TestConnectionResponse(
            status='error',
            message=f'Test failed: {str(e)}'
        )


@router.post("/tickets/{ticket_id}/create-jira-issue")
async def create_jira_issue_from_ticket(
    ticket_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create JIRA issue from ticket"""
    from app.models.ticket import Ticket
    
    # Get ticket
    result = await db.execute(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.tenant_id == tenant.id
        )
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Get JIRA integration
    result = await db.execute(
        select(Integration).where(
            Integration.tenant_id == tenant.id,
            Integration.type == 'jira',
            Integration.status == 'active'
        )
    )
    integration = result.scalar_one_or_none()
    
    if not integration:
        raise HTTPException(status_code=404, detail="No active JIRA integration found")
    
    # Create issue
    try:
        jira = JiraIntegration(integration.config)
        issue_key = await jira.create_issue({
            'title': ticket.title,
            'description': ticket.description,
            'priority': ticket.priority or ticket.ai_priority,
            'ai_summary': ticket.ai_summary,
            'ai_category': ticket.ai_category,
            'ai_intent': ticket.ai_intent
        })
        
        if issue_key:
            # Store JIRA issue key in ticket metadata
            if not ticket.metadata:
                ticket.metadata = {}
            ticket.metadata['jira_issue'] = issue_key
            await db.commit()
            
            return {
                'status': 'success',
                'message': f'Created JIRA issue: {issue_key}',
                'issue_key': issue_key
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create JIRA issue")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tickets/{ticket_id}/notify-slack")
async def send_slack_notification_for_ticket(
    ticket_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send Slack notification for ticket"""
    from app.models.ticket import Ticket
    
    # Get ticket
    result = await db.execute(
        select(Ticket).where(
            Ticket.id == ticket_id,
            Ticket.tenant_id == tenant.id
        )
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Get Slack integration
    result = await db.execute(
        select(Integration).where(
            Integration.tenant_id == tenant.id,
            Integration.type == 'slack',
            Integration.status == 'active'
        )
    )
    integration = result.scalar_one_or_none()
    
    if not integration:
        raise HTTPException(status_code=404, detail="No active Slack integration found")
    
    # Send notification
    try:
        slack = SlackIntegration(integration.config)
        success = await slack.send_notification({
            'id': str(ticket.id),
            'title': ticket.title,
            'customer_name': ticket.customer_name,
            'priority': ticket.priority,
            'ai_category': ticket.ai_category,
            'ai_sentiment': ticket.ai_sentiment,
            'ai_summary': ticket.ai_summary,
            'ai_suggested_actions': ticket.ai_suggested_actions
        })
        
        if success:
            return {
                'status': 'success',
                'message': 'Slack notification sent'
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send Slack notification")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
