"""
Pure SQL insertion using asyncpg directly - NO SQLAlchemy.
"""
import asyncio
import asyncpg
import os

async def insert_data():
    # Get and clean DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    db_url = db_url.replace('postgresql://', 'postgres://')
    db_url = db_url.replace('sslmode=require', '').replace('channel_binding=require', '')
    db_url = db_url.replace('?&', '?').replace('&&', '&')
    if db_url.endswith('?') or db_url.endswith('&'):
        db_url = db_url[:-1]
    
    print("🔌 Connecting to database...")
    conn = await asyncpg.connect(db_url, ssl='require')
    
    print("🗑️  Clearing existing data...")
    await conn.execute("DELETE FROM ai_analysis")
    await conn.execute("DELETE FROM tickets")
    print("✅ Cleared")
    
    print("\n📝 Inserting 5 tickets...")
    
    # Ticket 1
    await conn.execute("""
        INSERT INTO tickets (
            id, external_id, external_source, title, description,
            status, priority, category, subcategory, intent,
            customer_id, customer_email, customer_name, sla_due_at, sla_breached,
            tags, created_at, updated_at
        ) VALUES (
            '11111111-1111-1111-1111-111111111111', 'TKT-10001', 'email',
            'Package not delivered on time', 'Customer reported delayed shipment',
            'open', 'high', 'shipping', 'delayed_shipment', 'delayed_shipment',
            'c1111111-1111-1111-1111-111111111111', 'support@acme.com', 'Acme Corp', NOW() + INTERVAL '12 hours', false,
            '["shipping", "high"]'::jsonb, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'
        )
    """)
    print("  ✅ Ticket 1: Package not delivered")
    
    # Ticket 2
    await conn.execute("""
        INSERT INTO tickets (
            id, external_id, external_source, title, description,
            status, priority, category, subcategory, intent,
            customer_id, customer_email, customer_name, sla_due_at, sla_breached,
            tags, created_at, updated_at
        ) VALUES (
            '22222222-2222-2222-2222-222222222221', 'TKT-10002', 'chat',
            'Cannot log into account', 'Login credentials not working',
            'open', 'critical', 'login', 'login_failed', 'login_failed',
            'c2222222-2222-2222-2222-222222222222', 'help@techstart.io', 'TechStart Inc', NOW() + INTERVAL '2 hours', false,
            '["login", "critical"]'::jsonb, NOW() - INTERVAL '1 hour', NOW() - INTERVAL '1 hour'
        )
    """)
    print("  ✅ Ticket 2: Cannot log in")
    
    # Ticket 3
    await conn.execute("""
        INSERT INTO tickets (
            id, external_id, external_source, title, description,
            status, priority, category, subcategory, intent, assigned_to,
            customer_id, customer_email, customer_name, sla_due_at, sla_breached,
            tags, created_at, updated_at, resolved_at
        ) VALUES (
            '33333333-3333-3333-3333-333333333331', 'TKT-10003', 'web',
            'App crashes when trying to checkout', 'Payment screen causes crash',
            'resolved', 'urgent', 'app_crash', 'checkout_crash', 'checkout_crash', 'agent_1',
            'c3333333-3333-3333-3333-333333333333', 'service@globalretail.com', 'Global Retail', NOW() - INTERVAL '2 days', false,
            '["app_crash", "urgent"]'::jsonb, NOW() - INTERVAL '5 days', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'
        )
    """)
    print("  ✅ Ticket 3: App crash resolved")
    
    # Ticket 4
    await conn.execute("""
        INSERT INTO tickets (
            id, external_id, external_source, title, description,
            status, priority, category, subcategory, intent, assigned_to,
            customer_id, customer_email, customer_name, sla_due_at, sla_breached,
            tags, created_at, updated_at
        ) VALUES (
            '44444444-4444-4444-4444-444444444441', 'TKT-10004', 'email',
            'Payment declined but money charged', 'Double charge issue',
            'in_progress', 'urgent', 'payment', 'charge_dispute', 'charge_dispute', 'agent_2',
            'c4444444-4444-4444-4444-444444444444', 'support@fastship.co', 'FastShip Co', NOW() + INTERVAL '6 hours', false,
            '["payment", "urgent"]'::jsonb, NOW() - INTERVAL '4 hours', NOW() - INTERVAL '2 hours'
        )
    """)
    print("  ✅ Ticket 4: Payment issue")
    
    # Ticket 5
    await conn.execute("""
        INSERT INTO tickets (
            id, external_id, external_source, title, description,
            status, priority, category, subcategory, intent, assigned_to,
            customer_id, customer_email, customer_name, sla_due_at, sla_breached,
            tags, created_at, updated_at, resolved_at
        ) VALUES (
            '55555555-5555-5555-5555-555555555551', 'TKT-10005', 'web',
            'Product does not fit as expected', 'Size runs small',
            'resolved', 'low', 'sizing', 'wrong_size', 'wrong_size', 'agent_3',
            'c5555555-5555-5555-5555-555555555555', 'help@cloudbase.io', 'CloudBase', NOW() - INTERVAL '3 days', false,
            '["sizing", "low"]'::jsonb, NOW() - INTERVAL '7 days', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'
        )
    """)
    print("  ✅ Ticket 5: Sizing issue resolved")
    
    print("\n🤖 Inserting 5 AI analyses...")
    
    # Analysis 1
    await conn.execute("""
        INSERT INTO ai_analysis (
            id, ticket_id, sentiment, intent, urgency, category,
            priority_score, summary, suggested_actions, created_at
        ) VALUES (
            'a1111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111',
            35.0, 'delayed_shipment', 'high', 'shipping', 70.0,
            'Shipping delay. Customer frustrated. Requires logistics team attention.',
            '["Contact shipping carrier", "Provide tracking update", "Offer expedited shipping"]'::jsonb,
            NOW() - INTERVAL '1 day' + INTERVAL '5 minutes'
        )
    """)
    print("  ✅ Analysis 1")
    
    # Analysis 2
    await conn.execute("""
        INSERT INTO ai_analysis (
            id, ticket_id, sentiment, intent, urgency, category,
            priority_score, summary, suggested_actions, created_at
        ) VALUES (
            'a2222222-2222-2222-2222-222222222221', '22222222-2222-2222-2222-222222222221',
            18.0, 'login_failed', 'critical', 'login', 95.0,
            'Critical login failure. Customer locked out of account.',
            '["Reset password immediately", "Unlock account", "Escalate to engineering"]'::jsonb,
            NOW() - INTERVAL '1 hour' + INTERVAL '3 minutes'
        )
    """)
    print("  ✅ Analysis 2")
    
    # Analysis 3
    await conn.execute("""
        INSERT INTO ai_analysis (
            id, ticket_id, sentiment, intent, urgency, category,
            priority_score, summary, suggested_actions, created_at
        ) VALUES (
            'a3333333-3333-3333-3333-333333333331', '33333333-3333-3333-3333-333333333331',
            76.0, 'checkout_crash', 'urgent', 'app_crash', 85.0,
            'Checkout crash resolved. Performance optimization applied.',
            '["Deploy emergency patch", "Test payment flow", "Monitor error logs"]'::jsonb,
            NOW() - INTERVAL '5 days' + INTERVAL '10 minutes'
        )
    """)
    print("  ✅ Analysis 3")
    
    # Analysis 4
    await conn.execute("""
        INSERT INTO ai_analysis (
            id, ticket_id, sentiment, intent, urgency, category,
            priority_score, summary, suggested_actions, created_at
        ) VALUES (
            'a4444444-4444-4444-4444-444444444441', '44444444-4444-4444-4444-444444444441',
            20.0, 'charge_dispute', 'urgent', 'payment', 86.0,
            'Double charge reported. Customer very upset. Refund needed.',
            '["Issue immediate refund", "Investigate payment gateway", "Apologize to customer"]'::jsonb,
            NOW() - INTERVAL '4 hours' + INTERVAL '4 minutes'
        )
    """)
    print("  ✅ Analysis 4")
    
    # Analysis 5
    await conn.execute("""
        INSERT INTO ai_analysis (
            id, ticket_id, sentiment, intent, urgency, category,
            priority_score, summary, suggested_actions, created_at
        ) VALUES (
            'a5555555-5555-5555-5555-555555555551', '55555555-5555-5555-5555-555555555551',
            85.0, 'wrong_size', 'low', 'sizing', 28.0,
            'Size issue resolved. Customer satisfied with exchange.',
            '["Provide return label", "Suggest correct size", "Update size chart"]'::jsonb,
            NOW() - INTERVAL '7 days' + INTERVAL '10 minutes'
        )
    """)
    print("  ✅ Analysis 5")
    
    # Verify
    count = await conn.fetchval("SELECT COUNT(*) FROM tickets")
    print(f"\n✅ Total tickets: {count}")
    
    count2 = await conn.fetchval("SELECT COUNT(*) FROM ai_analysis")
    print(f"✅ Total AI analyses: {count2}")
    
    await conn.close()
    print("\n🎉 Mock data insertion complete!")

if __name__ == "__main__":
    asyncio.run(insert_data())
