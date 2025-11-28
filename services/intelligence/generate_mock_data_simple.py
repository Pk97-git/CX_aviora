"""
Simplified mock data generator using SQLAlchemy ORM.
"""
import asyncio
import uuid
from datetime import datetime, timedelta
import random
from app.core.database import AsyncSessionLocal
from app.models.database import Ticket, AIAnalysis
from sqlalchemy import text

# Mock data templates
CUSTOMERS = [
    {"id": "cust_001", "name": "Acme Corp", "email": "support@acme.com"},
    {"id": "cust_002", "name": "TechStart Inc", "email": "help@techstart.io"},
    {"id": "cust_003", "name": "Global Retail", "email": "service@globalretail.com"},
    {"id": "cust_004", "name": "FastShip Co", "email": "support@fastship.co"},
    {"id": "cust_005", "name": "CloudBase", "email": "help@cloudbase.io"},
]

CATEGORIES = {
    "shipping": ["delayed_shipment", "lost_package", "wrong_address"],
    "login": ["password_reset", "account_locked", "login_loop"],
    "sizing": ["wrong_size", "size_chart_unclear", "return_request"],
    "app_crash": ["ios_crash", "checkout_freeze", "search_broken"],
    "payment": ["payment_failed", "refund_request", "charge_dispute"],
}

TITLES = {
    "shipping": ["Package not delivered", "Tracking issue", "Wrong address"],
    "login": ["Can't log in", "Password reset not working", "Account locked"],
    "sizing": ["Wrong size received", "Size chart confusing", "Need to return"],
    "app_crash": ["App crashes on checkout", "Search not working", "App freezes"],
    "payment": ["Payment declined", "Refund not received", "Duplicate charge"],
}

STATUSES = ["open", "in_progress", "resolved", "closed"]
PRIORITIES = ["low", "medium", "high", "urgent", "critical"]
SOURCES = ["email", "chat", "phone", "web"]


async def generate_mock_data():
    """Generate and insert mock data."""
    print("🚀 Generating mock data...")
    
    async with AsyncSessionLocal() as session:
        # Clear existing data
        print("🗑️  Clearing existing data...")
        await session.execute(text("DELETE FROM ai_analysis"))
        await session.execute(text("DELETE FROM tickets"))
        await session.commit()
        print("✅ Cleared")
        
        now = datetime.utcnow()
        tickets_created = 0
        analyses_created = 0
        
        # Generate 50 tickets
        for i in range(50):
            days_ago = random.randint(0, 90)
            created_at = now - timedelta(days=days_ago)
            
            category = random.choice(list(CATEGORIES.keys()))
            intent = random.choice(CATEGORIES[category])
            title = random.choice(TITLES[category])
            customer = random.choice(CUSTOMERS)
            
            # Status based on age
            if days_ago > 60:
                status = random.choice(["resolved", "closed"])
            elif days_ago > 7:
                status = random.choice(["in_progress", "resolved"])
            else:
                status = random.choice(["open", "in_progress"])
            
            priority = random.choice(PRIORITIES)
            
            # SLA
            sla_hours = {"low": 72, "medium": 48, "high": 24, "urgent": 12, "critical": 4}
            sla_due_at = created_at + timedelta(hours=sla_hours[priority])
            sla_breached = 1 if (status in ["open", "in_progress"] and now > sla_due_at) else 0
            
            resolved_at = None
            if status in ["resolved", "closed"]:
                resolved_at = created_at + timedelta(hours=random.randint(1, sla_hours[priority]))
            
            # Create ticket
            ticket = Ticket(
                id=str(uuid.uuid4()),
                tenant_id="tenant_001",
                external_id=f"TKT-{10000 + i}",
                external_source=random.choice(SOURCES),
                title=title,
                description=f"Customer reported: {title}",
                status=status,
                priority=priority,
                category=category,
                subcategory=intent,
                intent=intent,
                assigned_to=None if status == "open" else f"agent_{random.randint(1, 5)}",
                customer_id=customer["id"],
                customer_email=customer["email"],
                customer_name=customer["name"],
                sla_due_at=sla_due_at,
                sla_breached=sla_breached,
                created_at=created_at,
                updated_at=created_at,
                resolved_at=resolved_at
            )
            session.add(ticket)
            tickets_created += 1
            
            # Create AI analysis
            if status in ["resolved", "closed"]:
                sentiment = random.uniform(70, 95)
            elif priority in ["critical", "urgent"]:
                sentiment = random.uniform(15, 40)
            else:
                sentiment = random.uniform(50, 80)
            
            priority_scores = {"low": 20, "medium": 40, "high": 60, "urgent": 80, "critical": 95}
            priority_score = priority_scores[priority] + random.uniform(-10, 10)
            
            analysis = AIAnalysis(
                id=str(uuid.uuid4()),
                ticket_id=ticket.id,
                sentiment=round(sentiment, 1),
                intent=intent,
                urgency=priority,
                category=category,
                priority_score=round(priority_score, 1),
                summary=f"{category.title()} issue. Sentiment: {'positive' if sentiment > 60 else 'negative'}.",
                suggested_actions=["Contact customer", "Escalate to team", "Provide update"],
                created_at=created_at + timedelta(minutes=5)
            )
            session.add(analysis)
            analyses_created += 1
        
        # Commit all
        await session.commit()
        print(f"\n🎉 Mock data generation complete!")
        print(f"   - {tickets_created} tickets created")
        print(f"   - {analyses_created} AI analyses created")


if __name__ == "__main__":
    asyncio.run(generate_mock_data())
