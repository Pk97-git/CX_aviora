"""
Admin endpoint to populate database with mock data.
Access: POST /admin/populate-mock-data
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/populate-mock-data")
async def populate_mock_data(db: AsyncSession = Depends(get_db)):
    """
    Populate database with mock data for testing.
    WARNING: This will clear existing data!
    """
    from app.models.database import Ticket, AIAnalysis
    from sqlalchemy import delete
    
    try:
        # Clear existing data
        await db.execute(delete(AIAnalysis))
        await db.execute(delete(Ticket))
        await db.commit()
        
        now = datetime.utcnow()
        tickets_created = 0
        analyses_created = 0
        
        # Ticket 1 - Open shipping issue
        ticket1 = Ticket(
            id=uuid.UUID('11111111-1111-1111-1111-111111111111'),
            tenant_id=uuid.UUID('00000000-0000-0000-0000-000000000001'),
            external_id='TKT-10001',
            external_source='email',
            title='Package not delivered on time',
            description='Customer reported delayed shipment',
            status='open',
            priority='high',
            category='shipping',
            subcategory='delayed_shipment',
            intent='delayed_shipment',
            customer_id=uuid.UUID('c1111111-1111-1111-1111-111111111111'),
            customer_email='support@acme.com',
            customer_name='Acme Corp',
            sla_due_at=now + timedelta(hours=12),
            sla_breached=False,
            tags=['shipping', 'high'],
            created_at=now - timedelta(days=1),
            updated_at=now - timedelta(days=1)
        )
        db.add(ticket1)
        tickets_created += 1
        
        # Ticket 2 - Critical login issue
        ticket2 = Ticket(
            id=uuid.UUID('22222222-2222-2222-2222-222222222221'),
            tenant_id=uuid.UUID('00000000-0000-0000-0000-000000000001'),
            external_id='TKT-10002',
            external_source='chat',
            title='Cannot log into account',
            description='Login credentials not working',
            status='open',
            priority='critical',
            category='login',
            subcategory='login_failed',
            intent='login_failed',
            customer_id=uuid.UUID('c2222222-2222-2222-2222-222222222222'),
            customer_email='help@techstart.io',
            customer_name='TechStart Inc',
            sla_due_at=now + timedelta(hours=2),
            sla_breached=False,
            tags=['login', 'critical'],
            created_at=now - timedelta(hours=1),
            updated_at=now - timedelta(hours=1)
        )
        db.add(ticket2)
        tickets_created += 1
        
        # Ticket 3 - Resolved app crash
        ticket3 = Ticket(
            id=uuid.UUID('33333333-3333-3333-3333-333333333331'),
            tenant_id=uuid.UUID('00000000-0000-0000-0000-000000000001'),
            external_id='TKT-10003',
            external_source='web',
            title='App crashes when trying to checkout',
            description='Payment screen causes crash',
            status='resolved',
            priority='urgent',
            category='app_crash',
            subcategory='checkout_crash',
            intent='checkout_crash',
            assigned_to=uuid.UUID('a0000000-0000-0000-0000-000000000001'),
            customer_id=uuid.UUID('c3333333-3333-3333-3333-333333333333'),
            customer_email='service@globalretail.com',
            customer_name='Global Retail',
            sla_due_at=now - timedelta(days=2),
            sla_breached=False,
            tags=['app_crash', 'urgent'],
            created_at=now - timedelta(days=5),
            updated_at=now - timedelta(days=2),
            resolved_at=now - timedelta(days=2)
        )
        db.add(ticket3)
        tickets_created += 1
        
        # Ticket 4 - Payment issue in progress
        ticket4 = Ticket(
            id=uuid.UUID('44444444-4444-4444-4444-444444444441'),
            tenant_id=uuid.UUID('00000000-0000-0000-0000-000000000001'),
            external_id='TKT-10004',
            external_source='email',
            title='Payment declined but money charged',
            description='Double charge issue',
            status='in_progress',
            priority='urgent',
            category='payment',
            subcategory='charge_dispute',
            intent='charge_dispute',
            assigned_to=uuid.UUID('a0000000-0000-0000-0000-000000000002'),
            customer_id=uuid.UUID('c4444444-4444-4444-4444-444444444444'),
            customer_email='support@fastship.co',
            customer_name='FastShip Co',
            sla_due_at=now + timedelta(hours=6),
            sla_breached=False,
            tags=['payment', 'urgent'],
            created_at=now - timedelta(hours=4),
            updated_at=now - timedelta(hours=2)
        )
        db.add(ticket4)
        tickets_created += 1
        
        # Ticket 5 - Sizing issue resolved
        ticket5 = Ticket(
            id=uuid.UUID('55555555-5555-5555-5555-555555555551'),
            tenant_id=uuid.UUID('00000000-0000-0000-0000-000000000001'),
            external_id='TKT-10005',
            external_source='web',
            title='Product does not fit as expected',
            description='Size runs small',
            status='resolved',
            priority='low',
            category='sizing',
            subcategory='wrong_size',
            intent='wrong_size',
            assigned_to=uuid.UUID('a0000000-0000-0000-0000-000000000003'),
            customer_id=uuid.UUID('c5555555-5555-5555-5555-555555555555'),
            customer_email='help@cloudbase.io',
            customer_name='CloudBase',
            sla_due_at=now - timedelta(days=3),
            sla_breached=False,
            tags=['sizing', 'low'],
            created_at=now - timedelta(days=7),
            updated_at=now - timedelta(days=3),
            resolved_at=now - timedelta(days=3)
        )
        db.add(ticket5)
        tickets_created += 1
        
        # Create AI analyses
        analysis1 = AIAnalysis(
            id=uuid.UUID('a1111111-1111-1111-1111-111111111111'),
            ticket_id=uuid.UUID('11111111-1111-1111-1111-111111111111'),
            sentiment=35.0,
            intent='delayed_shipment',
            urgency='high',
            category='shipping',
            priority_score=70.0,
            summary='Shipping delay. Customer frustrated. Requires logistics team attention.',
            suggested_actions=['Contact shipping carrier', 'Provide tracking update', 'Offer expedited shipping'],
            created_at=now - timedelta(days=1) + timedelta(minutes=5)
        )
        db.add(analysis1)
        analyses_created += 1
        
        analysis2 = AIAnalysis(
            id=uuid.UUID('a2222222-2222-2222-2222-222222222221'),
            ticket_id=uuid.UUID('22222222-2222-2222-2222-222222222221'),
            sentiment=18.0,
            intent='login_failed',
            urgency='critical',
            category='login',
            priority_score=95.0,
            summary='Critical login failure. Customer locked out of account.',
            suggested_actions=['Reset password immediately', 'Unlock account', 'Escalate to engineering'],
            created_at=now - timedelta(hours=1) + timedelta(minutes=3)
        )
        db.add(analysis2)
        analyses_created += 1
        
        analysis3 = AIAnalysis(
            id=uuid.UUID('a3333333-3333-3333-3333-333333333331'),
            ticket_id=uuid.UUID('33333333-3333-3333-3333-333333333331'),
            sentiment=76.0,
            intent='checkout_crash',
            urgency='urgent',
            category='app_crash',
            priority_score=85.0,
            summary='Checkout crash resolved. Performance optimization applied.',
            suggested_actions=['Deploy emergency patch', 'Test payment flow', 'Monitor error logs'],
            created_at=now - timedelta(days=5) + timedelta(minutes=10)
        )
        db.add(analysis3)
        analyses_created += 1
        
        analysis4 = AIAnalysis(
            id=uuid.UUID('a4444444-4444-4444-4444-444444444441'),
            ticket_id=uuid.UUID('44444444-4444-4444-4444-444444444441'),
            sentiment=20.0,
            intent='charge_dispute',
            urgency='urgent',
            category='payment',
            priority_score=86.0,
            summary='Double charge reported. Customer very upset. Refund needed.',
            suggested_actions=['Issue immediate refund', 'Investigate payment gateway', 'Apologize to customer'],
            created_at=now - timedelta(hours=4) + timedelta(minutes=4)
        )
        db.add(analysis4)
        analyses_created += 1
        
        analysis5 = AIAnalysis(
            id=uuid.UUID('a5555555-5555-5555-5555-555555555551'),
            ticket_id=uuid.UUID('55555555-5555-5555-5555-555555555551'),
            sentiment=85.0,
            intent='wrong_size',
            urgency='low',
            category='sizing',
            priority_score=28.0,
            summary='Size issue resolved. Customer satisfied with exchange.',
            suggested_actions=['Provide return label', 'Suggest correct size', 'Update size chart'],
            created_at=now - timedelta(days=7) + timedelta(minutes=10)
        )
        db.add(analysis5)
        analyses_created += 1
        
        await db.commit()
        
        return {
            "success": True,
            "message": "Mock data populated successfully",
            "tickets_created": tickets_created,
            "analyses_created": analyses_created
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to populate mock data: {str(e)}")
