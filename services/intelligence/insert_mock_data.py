"""
Direct SQL insertion with explicit transaction handling.
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine
from datetime import datetime, timedelta
import json

async def insert_mock_data():
    print("🚀 Starting mock data insertion...")
    
    async with engine.begin() as conn:
        # Clear existing data
        print("🗑️  Clearing existing data...")
        await conn.execute(text("DELETE FROM ai_analysis"))
        await conn.execute(text("DELETE FROM tickets"))
        print("✅ Cleared")
        
        # Insert 10 sample tickets (simplified for testing)
        tickets_data = []
        now = datetime.utcnow()
        
        # Ticket 1: Open shipping issue
        tickets_data.append({
            'id': '11111111-1111-1111-1111-111111111111',
            'tenant_id': 'tenant_001',
            'external_id': 'TKT-10001',
            'external_source': 'email',
            'title': 'Package not delivered on time',
            'description': 'Customer reported delayed shipment',
            'status': 'open',
            'priority': 'high',
            'category': 'shipping',
            'subcategory': 'delayed_shipment',
            'intent': 'delayed_shipment',
            'assigned_to': None,
            'customer_id': 'cust_001',
            'customer_email': 'support@acme.com',
            'customer_name': 'Acme Corp',
            'sla_due_at': now + timedelta(hours=12),
            'sla_breached': 0,
            'tags': json.dumps(['shipping', 'high']),
            'metadata': json.dumps({'source_ip': '192.168.1.1'}),
            'created_at': now - timedelta(days=1),
            'updated_at': now - timedelta(days=1),
            'resolved_at': None,
            'closed_at': None
        })
        
        # Ticket 2: Critical login issue
        tickets_data.append({
            'id': '22222222-2222-2222-2222-222222222221',
            'tenant_id': 'tenant_001',
            'external_id': 'TKT-10002',
            'external_source': 'chat',
            'title': 'Cannot log into account',
            'description': 'Login credentials not working',
            'status': 'open',
            'priority': 'critical',
            'category': 'login',
            'subcategory': 'login_failed',
            'intent': 'login_failed',
            'assigned_to': None,
            'customer_id': 'cust_002',
            'customer_email': 'help@techstart.io',
            'customer_name': 'TechStart Inc',
            'sla_due_at': now + timedelta(hours=2),
            'sla_breached': 0,
            'tags': json.dumps(['login', 'critical']),
            'metadata': json.dumps({'source_ip': '192.168.1.2'}),
            'created_at': now - timedelta(hours=1),
            'updated_at': now - timedelta(hours=1),
            'resolved_at': None,
            'closed_at': None
        })
        
        # Ticket 3: Resolved app crash
        tickets_data.append({
            'id': '33333333-3333-3333-3333-333333333331',
            'tenant_id': 'tenant_001',
            'external_id': 'TKT-10003',
            'external_source': 'web',
            'title': 'App crashes when trying to checkout',
            'description': 'Payment screen causes crash',
            'status': 'resolved',
            'priority': 'urgent',
            'category': 'app_crash',
            'subcategory': 'checkout_crash',
            'intent': 'checkout_crash',
            'assigned_to': 'agent_1',
            'customer_id': 'cust_003',
            'customer_email': 'service@globalretail.com',
            'customer_name': 'Global Retail',
            'sla_due_at': now - timedelta(days=2),
            'sla_breached': 0,
            'tags': json.dumps(['app_crash', 'urgent']),
            'metadata': json.dumps({'source_ip': '192.168.1.3'}),
            'created_at': now - timedelta(days=5),
            'updated_at': now - timedelta(days=2),
            'resolved_at': now - timedelta(days=2),
            'closed_at': None
        })
        
        # Ticket 4: Payment issue in progress
        tickets_data.append({
            'id': '44444444-4444-4444-4444-444444444441',
            'tenant_id': 'tenant_001',
            'external_id': 'TKT-10004',
            'external_source': 'email',
            'title': 'Payment declined but money charged',
            'description': 'Double charge issue',
            'status': 'in_progress',
            'priority': 'urgent',
            'category': 'payment',
            'subcategory': 'charge_dispute',
            'intent': 'charge_dispute',
            'assigned_to': 'agent_2',
            'customer_id': 'cust_004',
            'customer_email': 'support@fastship.co',
            'customer_name': 'FastShip Co',
            'sla_due_at': now + timedelta(hours=6),
            'sla_breached': 0,
            'tags': json.dumps(['payment', 'urgent']),
            'metadata': json.dumps({'source_ip': '192.168.1.4'}),
            'created_at': now - timedelta(hours=4),
            'updated_at': now - timedelta(hours=2),
            'resolved_at': None,
            'closed_at': None
        })
        
        # Ticket 5: Sizing issue resolved
        tickets_data.append({
            'id': '55555555-5555-5555-5555-555555555551',
            'tenant_id': 'tenant_001',
            'external_id': 'TKT-10005',
            'external_source': 'web',
            'title': 'Product does not fit as expected',
            'description': 'Size runs small',
            'status': 'resolved',
            'priority': 'low',
            'category': 'sizing',
            'subcategory': 'wrong_size',
            'intent': 'wrong_size',
            'assigned_to': 'agent_3',
            'customer_id': 'cust_005',
            'customer_email': 'help@cloudbase.io',
            'customer_name': 'CloudBase',
            'sla_due_at': now - timedelta(days=3),
            'sla_breached': 0,
            'tags': json.dumps(['sizing', 'low']),
            'metadata': json.dumps({'source_ip': '192.168.1.5'}),
            'created_at': now - timedelta(days=7),
            'updated_at': now - timedelta(days=3),
            'resolved_at': now - timedelta(days=3),
            'closed_at': None
        })
        
        # Insert tickets
        print(f"📝 Inserting {len(tickets_data)} tickets...")
        for i, ticket in enumerate(tickets_data, 1):
            try:
                # Convert datetime objects to ISO strings
                ticket_insert = {**ticket}
                for key in ['sla_due_at', 'created_at', 'updated_at', 'resolved_at', 'closed_at']:
                    if ticket_insert[key] is not None:
                        ticket_insert[key] = ticket_insert[key].isoformat()
                
                await conn.execute(
                    text("""
                        INSERT INTO tickets (
                            id, tenant_id, external_id, external_source, title, description,
                            status, priority, category, subcategory, intent, assigned_to,
                            customer_id, customer_email, customer_name, sla_due_at, sla_breached,
                            tags, metadata, created_at, updated_at, resolved_at, closed_at
                        ) VALUES (
                            :id, :tenant_id, :external_id, :external_source, :title, :description,
                            :status, :priority, :category, :subcategory, :intent, :assigned_to,
                            :customer_id, :customer_email, :customer_name, 
                            CAST(:sla_due_at AS timestamp), :sla_breached,
                            :tags::jsonb, :metadata::jsonb, 
                            CAST(:created_at AS timestamp), CAST(:updated_at AS timestamp), 
                            CAST(:resolved_at AS timestamp), CAST(:closed_at AS timestamp)
                        )
                    """),
                    ticket_insert
                )
                print(f"  ✅ Ticket {i}: {ticket['title']}")
            except Exception as e:
                print(f"  ❌ Ticket {i} failed: {e}")
                raise
        
        # Insert AI analyses
        print(f"\n🤖 Inserting AI analyses...")
        analyses = [
            {
                'id': 'a1111111-1111-1111-1111-111111111111',
                'ticket_id': '11111111-1111-1111-1111-111111111111',
                'sentiment': 35.0,
                'intent': 'delayed_shipment',
                'urgency': 'high',
                'category': 'shipping',
                'priority_score': 70.0,
                'summary': 'Shipping delay. Customer frustrated. Requires logistics team attention.',
                'suggested_actions': json.dumps(['Contact shipping carrier', 'Provide tracking update', 'Offer expedited shipping']),
                'created_at': now - timedelta(days=1) + timedelta(minutes=5)
            },
            {
                'id': 'a2222222-2222-2222-2222-222222222221',
                'ticket_id': '22222222-2222-2222-2222-222222222221',
                'sentiment': 18.0,
                'intent': 'login_failed',
                'urgency': 'critical',
                'category': 'login',
                'priority_score': 95.0,
                'summary': 'Critical login failure. Customer locked out of account.',
                'suggested_actions': json.dumps(['Reset password immediately', 'Unlock account', 'Escalate to engineering']),
                'created_at': now - timedelta(hours=1) + timedelta(minutes=3)
            },
            {
                'id': 'a3333333-3333-3333-3333-333333333331',
                'ticket_id': '33333333-3333-3333-3333-333333333331',
                'sentiment': 76.0,
                'intent': 'checkout_crash',
                'urgency': 'urgent',
                'category': 'app_crash',
                'priority_score': 85.0,
                'summary': 'Checkout crash resolved. Performance optimization applied.',
                'suggested_actions': json.dumps(['Deploy emergency patch', 'Test payment flow', 'Monitor error logs']),
                'created_at': now - timedelta(days=5) + timedelta(minutes=10)
            },
            {
                'id': 'a4444444-4444-4444-4444-444444444441',
                'ticket_id': '44444444-4444-4444-4444-444444444441',
                'sentiment': 20.0,
                'intent': 'charge_dispute',
                'urgency': 'urgent',
                'category': 'payment',
                'priority_score': 86.0,
                'summary': 'Double charge reported. Customer very upset. Refund needed.',
                'suggested_actions': json.dumps(['Issue immediate refund', 'Investigate payment gateway', 'Apologize to customer']),
                'created_at': now - timedelta(hours=4) + timedelta(minutes=4)
            },
            {
                'id': 'a5555555-5555-5555-5555-555555555551',
                'ticket_id': '55555555-5555-5555-5555-555555555551',
                'sentiment': 85.0,
                'intent': 'wrong_size',
                'urgency': 'low',
                'category': 'sizing',
                'priority_score': 28.0,
                'summary': 'Size issue resolved. Customer satisfied with exchange.',
                'suggested_actions': json.dumps(['Provide return label', 'Suggest correct size', 'Update size chart']),
                'created_at': now - timedelta(days=7) + timedelta(minutes=10)
            }
        ]
        
        for i, analysis in enumerate(analyses, 1):
            try:
                # Convert datetime to ISO string
                analysis_insert = {**analysis}
                if analysis_insert['created_at'] is not None:
                    analysis_insert['created_at'] = analysis_insert['created_at'].isoformat()
                
                await conn.execute(
                    text("""
                        INSERT INTO ai_analysis (
                            id, ticket_id, sentiment, intent, urgency, category,
                            priority_score, summary, suggested_actions, created_at
                        ) VALUES (
                            :id, :ticket_id, :sentiment, :intent, :urgency, :category,
                            :priority_score, :summary, :suggested_actions::jsonb, CAST(:created_at AS timestamp)
                        )
                    """),
                    analysis_insert
                )
                print(f"  ✅ Analysis {i}")
            except Exception as e:
                print(f"  ❌ Analysis {i} failed: {e}")
                raise
    
    print("\n🎉 Mock data insertion complete!")
    print("   - 5 tickets created")
    print("   - 5 AI analyses created")

if __name__ == "__main__":
    asyncio.run(insert_mock_data())
