"""
Comprehensive mock data generator for Aivora Intelligence Platform.
Generates realistic tickets and AI analysis data for testing.
"""
import asyncio
import uuid
import json
from datetime import datetime, timedelta
import random
from sqlalchemy import text
from app.core.database import engine

# Mock data templates
CUSTOMERS = [
    {"id": "cust_001", "name": "Acme Corp", "email": "support@acme.com"},
    {"id": "cust_002", "name": "TechStart Inc", "email": "help@techstart.io"},
    {"id": "cust_003", "name": "Global Retail", "email": "service@globalretail.com"},
    {"id": "cust_004", "name": "FastShip Co", "email": "support@fastship.co"},
    {"id": "cust_005", "name": "CloudBase", "email": "help@cloudbase.io"},
    {"id": "cust_006", "name": "DataFlow Ltd", "email": "support@dataflow.com"},
    {"id": "cust_007", "name": "MegaMart", "email": "cs@megamart.com"},
    {"id": "cust_008", "name": "QuickPay Inc", "email": "help@quickpay.com"},
    {"id": "cust_009", "name": "StyleHub", "email": "support@stylehub.com"},
    {"id": "cust_010", "name": "TechGear Pro", "email": "service@techgear.pro"},
]

CATEGORIES = {
    "shipping": {
        "intents": ["delayed_shipment", "lost_package", "wrong_address", "tracking_issue"],
        "titles": [
            "Package not delivered on time",
            "Tracking shows delivered but I didn't receive it",
            "Wrong shipping address used",
            "Shipment stuck in transit for 5 days",
            "Delivery attempted but no one was home"
        ]
    },
    "login": {
        "intents": ["password_reset", "account_locked", "login_loop", "2fa_issue"],
        "titles": [
            "Can't log into my account",
            "Password reset link not working",
            "Account locked after multiple attempts",
            "Stuck in login loop on iOS app",
            "2FA code not arriving"
        ]
    },
    "sizing": {
        "intents": ["wrong_size", "size_chart_unclear", "return_request", "exchange_needed"],
        "titles": [
            "Product doesn't fit as expected",
            "Size chart was confusing",
            "Need to return and get different size",
            "Item runs small, want to exchange",
            "Ordered wrong size, how to return?"
        ]
    },
    "app_crash": {
        "intents": ["ios_crash", "android_crash", "checkout_freeze", "search_broken"],
        "titles": [
            "App crashes when I try to checkout",
            "Search function not working",
            "App freezes on product page",
            "Can't complete purchase, app crashes",
            "Login screen keeps crashing"
        ]
    },
    "payment": {
        "intents": ["payment_failed", "refund_request", "charge_dispute", "payment_method_issue"],
        "titles": [
            "Payment declined but money was charged",
            "Refund not received after 7 days",
            "Duplicate charge on my card",
            "Can't add new payment method",
            "Transaction failed but order shows pending"
        ]
    },
    "returns": {
        "intents": ["return_policy", "return_label", "refund_status", "damaged_item"],
        "titles": [
            "How do I return this item?",
            "Return label not in package",
            "Item arrived damaged, need return",
            "Return processed but no refund yet",
            "Want to return but past 30 days"
        ]
    }
}

STATUSES = ["open", "in_progress", "pending_approval", "resolved", "closed"]
PRIORITIES = ["low", "medium", "high", "urgent", "critical"]
SOURCES = ["email", "chat", "phone", "web", "api"]

SUGGESTED_ACTIONS = {
    "shipping": [
        "Contact shipping carrier for status update",
        "Issue replacement shipment",
        "Provide tracking number update",
        "Offer expedited shipping for next order"
    ],
    "login": [
        "Send password reset link",
        "Unlock account manually",
        "Clear session cache",
        "Escalate to engineering team"
    ],
    "sizing": [
        "Provide size chart link",
        "Offer free return label",
        "Suggest alternative size",
        "Update product description"
    ],
    "app_crash": [
        "Report to engineering team",
        "Suggest clearing app cache",
        "Recommend app update",
        "Provide web alternative"
    ],
    "payment": [
        "Verify payment with processor",
        "Issue refund immediately",
        "Escalate to billing team",
        "Update payment method"
    ],
    "returns": [
        "Send return label via email",
        "Process refund",
        "Approve return exception",
        "Provide return instructions"
    ]
}


def generate_ticket_data(num_tickets=50):
    """Generate realistic ticket data."""
    tickets = []
    now = datetime.utcnow()
    
    for i in range(num_tickets):
        # Random date in last 90 days
        days_ago = random.randint(0, 90)
        created_at = now - timedelta(days=days_ago)
        
        # Pick category and details
        category = random.choice(list(CATEGORIES.keys()))
        cat_data = CATEGORIES[category]
        intent = random.choice(cat_data["intents"])
        title = random.choice(cat_data["titles"])
        
        # Pick customer
        customer = random.choice(CUSTOMERS)
        
        # Determine status based on age
        if days_ago > 60:
            status = random.choice(["resolved", "closed"])
        elif days_ago > 30:
            status = random.choice(["resolved", "closed", "in_progress"])
        elif days_ago > 7:
            status = random.choice(["in_progress", "pending_approval", "resolved"])
        else:
            status = random.choice(["open", "in_progress"])
        
        # Priority correlates with category
        if category in ["app_crash", "payment"]:
            priority = random.choice(["high", "urgent", "critical"])
        elif category in ["shipping", "login"]:
            priority = random.choice(["medium", "high", "urgent"])
        else:
            priority = random.choice(["low", "medium", "high"])
        
        # SLA based on priority
        sla_hours = {"low": 72, "medium": 48, "high": 24, "urgent": 12, "critical": 4}
        sla_due_at = created_at + timedelta(hours=sla_hours[priority])
        sla_breached = 1 if (status in ["open", "in_progress"] and now > sla_due_at) else 0
        
        # Resolved/closed dates
        resolved_at = None
        closed_at = None
        updated_at = created_at
        
        if status in ["resolved", "closed"]:
            resolution_hours = random.randint(1, sla_hours[priority] * 2)
            resolved_at = created_at + timedelta(hours=resolution_hours)
            updated_at = resolved_at
            if status == "closed":
                closed_at = resolved_at + timedelta(hours=random.randint(1, 24))
                updated_at = closed_at
        elif status == "in_progress":
            updated_at = created_at + timedelta(hours=random.randint(1, 48))
        
        # Assignee for non-open tickets
        assigned_to = None if status == "open" else f"agent_{random.randint(1, 10)}"
        
        ticket = {
            "id": str(uuid.uuid4()),
            "tenant_id": "tenant_001",
            "external_id": f"TKT-{10000 + i}",
            "external_source": random.choice(SOURCES),
            "title": title,
            "description": f"Customer reported: {title}. Ticket created via {random.choice(SOURCES)}.",
            "status": status,
            "priority": priority,
            "category": category,
            "subcategory": intent,
            "intent": intent,
            "sentiment": None,  # Will be set by AI analysis
            "urgency_score": None,  # Will be set by AI analysis
            "entities": None,
            "assigned_to": assigned_to,
            "customer_id": customer["id"],
            "customer_email": customer["email"],
            "customer_name": customer["name"],
            "sla_due_at": sla_due_at,
            "sla_breached": sla_breached,
            "tags": [category, priority],
            "metadata": {"source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"},
            "created_at": created_at,
            "updated_at": updated_at,
            "resolved_at": resolved_at,
            "closed_at": closed_at
        }
        
        tickets.append(ticket)
    
    return tickets


def generate_ai_analysis(ticket):
    """Generate AI analysis for a ticket."""
    category = ticket["category"]
    status = ticket["status"]
    priority = ticket["priority"]
    
    # Sentiment correlates with status and priority
    if status in ["resolved", "closed"]:
        sentiment = random.uniform(70, 95)
    elif priority in ["critical", "urgent"]:
        sentiment = random.uniform(15, 40)
    elif priority == "high":
        sentiment = random.uniform(35, 60)
    else:
        sentiment = random.uniform(50, 80)
    
    # Priority score
    priority_scores = {"low": 20, "medium": 40, "high": 60, "urgent": 80, "critical": 95}
    priority_score = priority_scores[priority] + random.uniform(-10, 10)
    priority_score = max(0, min(100, priority_score))
    
    # Summary
    summaries = {
        "shipping": f"Customer experiencing shipping delays. Sentiment: {'positive' if sentiment > 60 else 'negative'}. Requires logistics team attention.",
        "login": f"Account access issue reported. User frustrated with login process. Priority: {priority}.",
        "sizing": f"Product sizing concern. Customer requesting return/exchange. Moderate urgency.",
        "app_crash": f"Critical app stability issue. Affects user experience. Engineering escalation needed.",
        "payment": f"Payment processing problem. Financial impact. Requires immediate billing team review.",
        "returns": f"Return request submitted. Customer seeking refund/exchange. Standard processing."
    }
    
    # Suggested actions
    actions = random.sample(SUGGESTED_ACTIONS[category], k=random.randint(2, 4))
    
    analysis = {
        "id": str(uuid.uuid4()),
        "ticket_id": ticket["id"],
        "sentiment": round(sentiment, 1),
        "intent": ticket["intent"],
        "urgency": priority,
        "category": category,
        "priority_score": round(priority_score, 1),
        "summary": summaries.get(category, "Customer support request received."),
        "suggested_actions": actions,
        "created_at": ticket["created_at"] + timedelta(minutes=random.randint(1, 30))
    }
    
    return analysis


async def insert_mock_data():
    """Insert mock data into database."""
    print("🚀 Generating mock data...")
    
    # Generate tickets
    tickets = generate_ticket_data(50)
    print(f"✅ Generated {len(tickets)} tickets")
    
    # Generate AI analysis
    analyses = [generate_ai_analysis(ticket) for ticket in tickets]
    print(f"✅ Generated {len(analyses)} AI analyses")
    
    async with engine.begin() as conn:
        # Clear existing data
        print("🗑️  Clearing existing data...")
        await conn.execute(text("DELETE FROM ai_analysis"))
        await conn.execute(text("DELETE FROM tickets"))
        print("✅ Cleared existing data")
        
        # Insert tickets
        print("📝 Inserting tickets...")
        for ticket in tickets:
            # Convert datetime objects to ISO strings
            ticket_data = {**ticket}
            for key in ['created_at', 'updated_at', 'sla_due_at', 'resolved_at', 'closed_at']:
                if ticket_data[key] is not None:
                    ticket_data[key] = ticket_data[key].isoformat()
            
            await conn.execute(
                text("""
                    INSERT INTO tickets (
                        id, tenant_id, external_id, external_source, title, description,
                        status, priority, category, subcategory, intent, sentiment,
                        urgency_score, entities, assigned_to, customer_id, customer_email,
                        customer_name, sla_due_at, sla_breached, tags, metadata,
                        created_at, updated_at, resolved_at, closed_at
                    ) VALUES (
                        :id, :tenant_id, :external_id, :external_source, :title, :description,
                        :status, :priority, :category, :subcategory, :intent, :sentiment,
                        :urgency_score, :entities, :assigned_to, :customer_id, :customer_email,
                        :customer_name, :sla_due_at, :sla_breached, :tags::jsonb, :metadata::jsonb,
                        :created_at, :updated_at, :resolved_at, :closed_at
                    )
                """),
                {**ticket_data, "tags": json.dumps(ticket["tags"]), "metadata": json.dumps(ticket["metadata"])}
            )
        print(f"✅ Inserted {len(tickets)} tickets")
        
        # Insert AI analyses
        print("🤖 Inserting AI analyses...")
        for analysis in analyses:
            # Convert datetime to ISO string
            analysis_data = {**analysis}
            if analysis_data['created_at'] is not None:
                analysis_data['created_at'] = analysis_data['created_at'].isoformat()
            
            await conn.execute(
                text("""
                    INSERT INTO ai_analysis (
                        id, ticket_id, sentiment, intent, urgency, category,
                        priority_score, summary, suggested_actions, created_at
                    ) VALUES (
                        :id, :ticket_id, :sentiment, :intent, :urgency, :category,
                        :priority_score, :summary, :suggested_actions::jsonb, :created_at
                    )
                """),
                {**analysis_data, "suggested_actions": json.dumps(analysis["suggested_actions"])}
            )
        print(f"✅ Inserted {len(analyses)} AI analyses")
    
    print("\n🎉 Mock data generation complete!")
    print(f"   - {len(tickets)} tickets created")
    print(f"   - {len(analyses)} AI analyses created")
    print(f"   - Date range: Last 90 days")
    print(f"   - {len(CUSTOMERS)} unique customers")
    print(f"   - {len(CATEGORIES)} categories")


if __name__ == "__main__":
    asyncio.run(insert_mock_data())
