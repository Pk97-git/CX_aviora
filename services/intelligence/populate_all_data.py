"""
Populate all production database tables with realistic data.
"""
import asyncio
import asyncpg
import os
from datetime import datetime, timedelta, date
import random
import json
from uuid import uuid4

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Clean URL for asyncpg
if "sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0] + "?ssl=require"

# ===== POLICIES DATA =====
POLICIES_DATA = [
    {
        "name": "Refund Thresholds",
        "description": "Auto-approve refunds under $50. Require manager approval for >$500.",
        "status": "active",
        "compliance_score": 100.0,
        "rule_definition": {"threshold_low": 50, "threshold_high": 500, "auto_approve": True}
    },
    {
        "name": "PII Redaction",
        "description": "Automatically redact credit card numbers and SSNs from chat logs.",
        "status": "active",
        "compliance_score": 99.9,
        "rule_definition": {"patterns": ["credit_card", "ssn"], "action": "redact"}
    },
    {
        "name": "Tone & Brand Voice",
        "description": "Ensure agent replies match the 'Empathetic & Professional' persona.",
        "status": "monitoring",
        "compliance_score": 85.0,
        "rule_definition": {"persona": "empathetic_professional", "check_sentiment": True}
    },
    {
        "name": "Response Time SLA",
        "description": "First response within 2 hours for all tickets.",
        "status": "active",
        "compliance_score": 92.5,
        "rule_definition": {"max_response_time_hours": 2, "priority_override": True}
    },
    {
        "name": "Escalation Rules",
        "description": "Auto-escalate VIP customer issues to senior team.",
        "status": "active",
        "compliance_score": 98.0,
        "rule_definition": {"vip_tag": True, "escalate_to": "senior_team"}
    },
    {
        "name": "Data Retention",
        "description": "Archive closed tickets after 90 days, delete after 2 years.",
        "status": "active",
        "compliance_score": 100.0,
        "rule_definition": {"archive_days": 90, "delete_days": 730}
    },
    {
        "name": "Quality Assurance",
        "description": "Random sampling of 10% of resolved tickets for QA review.",
        "status": "active",
        "compliance_score": 88.5,
        "rule_definition": {"sample_rate": 0.1, "review_required": True}
    },
    {
        "name": "Spam Detection",
        "description": "Automatically flag and quarantine suspected spam tickets.",
        "status": "active",
        "compliance_score": 95.0,
        "rule_definition": {"confidence_threshold": 0.8, "action": "quarantine"}
    },
    {
        "name": "GDPR Compliance",
        "description": "Honor data deletion requests within 30 days.",
        "status": "active",
        "compliance_score": 100.0,
        "rule_definition": {"max_days": 30, "verification_required": True}
    },
    {
        "name": "Agent Workload Limits",
        "description": "Maximum 15 concurrent tickets per agent.",
        "status": "monitoring",
        "compliance_score": 78.0,
        "rule_definition": {"max_concurrent": 15, "enforce": False}
    }
]

# ===== WORKFLOWS DATA =====
WORKFLOWS_DATA = [
    {
        "name": "High Value Refund Approval",
        "trigger_condition": "Ticket Created > $500",
        "actions": ["Check LTV", "Route to Manager", "Slack Alert"],
        "status": "active",
        "total_runs": 145,
        "success_count": 142,
        "time_saved_hours": 24.0
    },
    {
        "name": "Auto-Reply: Shipping Delays",
        "trigger_condition": "Intent = 'Shipping Status'",
        "actions": ["Check Order Status", "Send Email"],
        "status": "active",
        "total_runs": 1250,
        "success_count": 1248,
        "time_saved_hours": 180.0
    },
    {
        "name": "VIP Escalation",
        "trigger_condition": "Customer Tag = 'VIP'",
        "actions": ["Set Priority = Urgent", "Assign to Senior Team"],
        "status": "paused",
        "total_runs": 45,
        "success_count": 44,
        "time_saved_hours": 5.0
    },
    {
        "name": "Password Reset Auto-Response",
        "trigger_condition": "Category = 'Login Issue'",
        "actions": ["Send Reset Link", "Close Ticket"],
        "status": "active",
        "total_runs": 890,
        "success_count": 885,
        "time_saved_hours": 120.0
    },
    {
        "name": "Duplicate Ticket Merger",
        "trigger_condition": "Similar Title Detected",
        "actions": ["Merge Tickets", "Notify Customer"],
        "status": "active",
        "total_runs": 234,
        "success_count": 230,
        "time_saved_hours": 35.0
    },
    {
        "name": "Sentiment-Based Routing",
        "trigger_condition": "Sentiment = 'Frustrated'",
        "actions": ["Route to Experienced Agent", "Flag for Review"],
        "status": "active",
        "total_runs": 567,
        "success_count": 565,
        "time_saved_hours": 78.0
    },
    {
        "name": "Invoice Generation",
        "trigger_condition": "Request Type = 'Invoice'",
        "actions": ["Generate PDF", "Email to Customer"],
        "status": "active",
        "total_runs": 423,
        "success_count": 421,
        "time_saved_hours": 60.0
    },
    {
        "name": "SLA Breach Alert",
        "trigger_condition": "SLA Due in 1 Hour",
        "actions": ["Notify Agent", "Escalate if Needed"],
        "status": "active",
        "total_runs": 178,
        "success_count": 175,
        "time_saved_hours": 25.0
    },
    {
        "name": "Post-Resolution Survey",
        "trigger_condition": "Ticket Status = 'Resolved'",
        "actions": ["Send CSAT Survey", "Track Response"],
        "status": "active",
        "total_runs": 2100,
        "success_count": 2095,
        "time_saved_hours": 280.0
    },
    {
        "name": "Bulk Order Discount",
        "trigger_condition": "Quantity > 100",
        "actions": ["Calculate Discount", "Send Quote"],
        "status": "active",
        "total_runs": 89,
        "success_count": 88,
        "time_saved_hours": 12.0
    },
    {
        "name": "After-Hours Auto-Reply",
        "trigger_condition": "Time = Outside Business Hours",
        "actions": ["Send Auto-Reply", "Queue for Next Day"],
        "status": "active",
        "total_runs": 1567,
        "success_count": 1565,
        "time_saved_hours": 210.0
    },
    {
        "name": "Product Recommendation",
        "trigger_condition": "Intent = 'Product Inquiry'",
        "actions": ["Analyze Preferences", "Suggest Products"],
        "status": "active",
        "total_runs": 345,
        "success_count": 340,
        "time_saved_hours": 48.0
    },
    {
        "name": "Churn Risk Detection",
        "trigger_condition": "Multiple Complaints",
        "actions": ["Flag Customer", "Offer Retention Incentive"],
        "status": "monitoring",
        "total_runs": 67,
        "success_count": 65,
        "time_saved_hours": 9.0
    },
    {
        "name": "Knowledge Base Suggestion",
        "trigger_condition": "Common Question Detected",
        "actions": ["Suggest KB Article", "Auto-Resolve if Accepted"],
        "status": "active",
        "total_runs": 1890,
        "success_count": 1875,
        "time_saved_hours": 250.0
    },
    {
        "name": "Priority Adjustment",
        "trigger_condition": "Urgency Score > 0.8",
        "actions": ["Increase Priority", "Notify Team Lead"],
        "status": "active",
        "total_runs": 456,
        "success_count": 453,
        "time_saved_hours": 62.0
    }
]

# ===== TOPIC CLUSTERS =====
TOPICS_DATA = [
    {"topic": "Payment Issues", "volume": 245, "trend": "rising", "keywords": ["payment", "declined", "card", "billing"], "avg_sentiment": -0.4},
    {"topic": "Shipping Delays", "volume": 189, "trend": "stable", "keywords": ["shipping", "delivery", "tracking", "late"], "avg_sentiment": -0.3},
    {"topic": "Login Problems", "volume": 156, "trend": "falling", "keywords": ["login", "password", "account", "access"], "avg_sentiment": -0.5},
    {"topic": "Product Quality", "volume": 134, "trend": "rising", "keywords": ["quality", "defect", "broken", "damaged"], "avg_sentiment": -0.6},
    {"topic": "Refund Requests", "volume": 123, "trend": "stable", "keywords": ["refund", "return", "money back"], "avg_sentiment": -0.2},
    {"topic": "Feature Requests", "volume": 98, "trend": "rising", "keywords": ["feature", "request", "add", "new"], "avg_sentiment": 0.3},
    {"topic": "Account Management", "volume": 87, "trend": "stable", "keywords": ["account", "update", "change", "settings"], "avg_sentiment": 0.1},
    {"topic": "Technical Support", "volume": 76, "trend": "falling", "keywords": ["technical", "bug", "error", "crash"], "avg_sentiment": -0.4},
    {"topic": "Billing Inquiries", "volume": 65, "trend": "stable", "keywords": ["billing", "invoice", "charge", "subscription"], "avg_sentiment": -0.1},
    {"topic": "Product Recommendations", "volume": 54, "trend": "rising", "keywords": ["recommend", "suggest", "similar", "alternative"], "avg_sentiment": 0.4},
    {"topic": "Cancellation Requests", "volume": 43, "trend": "rising", "keywords": ["cancel", "unsubscribe", "stop"], "avg_sentiment": -0.3},
    {"topic": "Order Tracking", "volume": 38, "trend": "stable", "keywords": ["track", "order", "status", "where"], "avg_sentiment": 0.0},
    {"topic": "Promo Code Issues", "volume": 32, "trend": "falling", "keywords": ["promo", "code", "discount", "coupon"], "avg_sentiment": -0.2},
    {"topic": "Customer Feedback", "volume": 28, "trend": "stable", "keywords": ["feedback", "review", "rating", "experience"], "avg_sentiment": 0.5},
    {"topic": "Warranty Claims", "volume": 21, "trend": "stable", "keywords": ["warranty", "claim", "coverage", "repair"], "avg_sentiment": -0.1}
]

# ===== REGIONAL DATA =====
REGIONAL_DATA = [
    {"region": "North America", "country_code": "US", "volume": 450, "avg_sentiment": 0.2, "top_issues": ["Payment Issues", "Shipping Delays"], "resolution_rate": 0.85},
    {"region": "Europe", "country_code": "GB", "volume": 320, "avg_sentiment": 0.3, "top_issues": ["Product Quality", "Refund Requests"], "resolution_rate": 0.88},
    {"region": "Asia Pacific", "country_code": "SG", "volume": 280, "avg_sentiment": 0.1, "top_issues": ["Login Problems", "Technical Support"], "resolution_rate": 0.82},
    {"region": "Latin America", "country_code": "BR", "volume": 150, "avg_sentiment": 0.0, "top_issues": ["Shipping Delays", "Payment Issues"], "resolution_rate": 0.78},
    {"region": "Middle East", "country_code": "AE", "volume": 95, "avg_sentiment": 0.2, "top_issues": ["Product Quality", "Billing Inquiries"], "resolution_rate": 0.83},
    {"region": "Africa", "country_code": "ZA", "volume": 65, "avg_sentiment": 0.1, "top_issues": ["Payment Issues", "Account Management"], "resolution_rate": 0.75},
    {"region": "Australia", "country_code": "AU", "volume": 120, "avg_sentiment": 0.4, "top_issues": ["Feature Requests", "Product Recommendations"], "resolution_rate": 0.90},
    {"region": "India", "country_code": "IN", "volume": 200, "avg_sentiment": 0.0, "top_issues": ["Technical Support", "Login Problems"], "resolution_rate": 0.80}
]

# ===== CHURN PREDICTIONS =====
CHURN_DATA = [
    {"segment": "High-Value Customers", "risk_score": 0.75, "affected_customers": 45, "risk_factors": ["Multiple complaints", "Delayed resolutions"], "recommended_actions": ["Personal outreach", "Offer premium support"]},
    {"segment": "Recent Signups", "risk_score": 0.45, "affected_customers": 120, "risk_factors": ["Onboarding issues", "Feature confusion"], "recommended_actions": ["Improve onboarding", "Send tutorial emails"]},
    {"segment": "Long-term Users", "risk_score": 0.30, "affected_customers": 80, "risk_factors": ["Lack of engagement", "Competitor offers"], "recommended_actions": ["Re-engagement campaign", "Loyalty rewards"]},
    {"segment": "Price-Sensitive", "risk_score": 0.65, "affected_customers": 95, "risk_factors": ["Price increases", "Better alternatives"], "recommended_actions": ["Offer discounts", "Highlight value"]},
    {"segment": "Enterprise Clients", "risk_score": 0.20, "affected_customers": 15, "risk_factors": ["Contract renewal", "Feature gaps"], "recommended_actions": ["Executive review", "Custom solutions"]},
    {"segment": "Trial Users", "risk_score": 0.85, "affected_customers": 200, "risk_factors": ["Low activation", "No payment method"], "recommended_actions": ["Activation emails", "Demo calls"]},
    {"segment": "Dormant Accounts", "risk_score": 0.90, "affected_customers": 150, "risk_factors": ["No recent activity", "Unresolved issues"], "recommended_actions": ["Win-back campaign", "Survey feedback"]},
    {"segment": "Support-Heavy Users", "risk_score": 0.55, "affected_customers": 60, "risk_factors": ["Frequent issues", "Low satisfaction"], "recommended_actions": ["Proactive support", "Product improvements"]},
    {"segment": "Mobile-Only Users", "risk_score": 0.40, "affected_customers": 110, "risk_factors": ["App issues", "Limited features"], "recommended_actions": ["Mobile optimization", "Feature parity"]},
    {"segment": "International Users", "risk_score": 0.50, "affected_customers": 75, "risk_factors": ["Localization gaps", "Payment issues"], "recommended_actions": ["Localization", "Regional payment methods"]}
]

# ===== FRICTION COSTS =====
FRICTION_DATA = [
    {"friction_point": "Payment Gateway Failures", "category": "Payment", "cost": 4500.0, "ticket_count": 145, "impact_score": 9.2, "difficulty": "hard"},
    {"friction_point": "Slow Checkout Process", "category": "Payment", "cost": 2100.0, "ticket_count": 89, "impact_score": 7.5, "difficulty": "medium"},
    {"friction_point": "Shipping Address Validation", "category": "Shipping", "cost": 1800.0, "ticket_count": 67, "impact_score": 6.8, "difficulty": "easy"},
    {"friction_point": "Product Image Quality", "category": "Product", "cost": 3200.0, "ticket_count": 45, "impact_score": 8.1, "difficulty": "medium"},
    {"friction_point": "Password Reset Flow", "category": "Login", "cost": 800.0, "ticket_count": 156, "impact_score": 5.5, "difficulty": "easy"},
    {"friction_point": "Search Functionality", "category": "Navigation", "cost": 1500.0, "ticket_count": 78, "impact_score": 6.2, "difficulty": "medium"},
    {"friction_point": "Mobile App Crashes", "category": "Technical", "cost": 5200.0, "ticket_count": 92, "impact_score": 9.8, "difficulty": "hard"},
    {"friction_point": "Promo Code Application", "category": "Payment", "cost": 900.0, "ticket_count": 32, "impact_score": 4.5, "difficulty": "easy"},
    {"friction_point": "Order Tracking Accuracy", "category": "Shipping", "cost": 1200.0, "ticket_count": 54, "impact_score": 5.8, "difficulty": "medium"},
    {"friction_point": "Customer Support Wait Times", "category": "Support", "cost": 6800.0, "ticket_count": 234, "impact_score": 9.5, "difficulty": "hard"},
    {"friction_point": "Return Process Complexity", "category": "Returns", "cost": 2800.0, "ticket_count": 123, "impact_score": 7.8, "difficulty": "medium"},
    {"friction_point": "Email Notification Delays", "category": "Communication", "cost": 600.0, "ticket_count": 43, "impact_score": 3.9, "difficulty": "easy"}
]


async def populate_all_data():
    """Populate all production tables with data"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("🚀 Populating production database...")
        
        # ===== POLICIES =====
        print("\n📋 Inserting policies...")
        for policy in POLICIES_DATA:
            await conn.execute("""
                INSERT INTO policies (id, name, description, status, compliance_score, rule_definition, violations_count, last_updated, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """, str(uuid4()), policy["name"], policy["description"], policy["status"],
                policy["compliance_score"], json.dumps(policy["rule_definition"]), 
                random.randint(0, 10), datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                datetime.utcnow() - timedelta(days=random.randint(30, 90)))
        print(f"✅ Inserted {len(POLICIES_DATA)} policies")
        
        # ===== WORKFLOWS =====
        print("\n⚙️ Inserting workflows...")
        for workflow in WORKFLOWS_DATA:
            await conn.execute("""
                INSERT INTO workflows (id, name, trigger_condition, actions, status, total_runs, success_count, failure_count, time_saved_hours, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """, str(uuid4()), workflow["name"], workflow["trigger_condition"],
                json.dumps(workflow["actions"]), workflow["status"], workflow["total_runs"],
                workflow["success_count"], workflow["total_runs"] - workflow["success_count"],
                workflow["time_saved_hours"], datetime.utcnow() - timedelta(days=random.randint(60, 180)),
                datetime.utcnow() - timedelta(days=random.randint(1, 7)))
        print(f"✅ Inserted {len(WORKFLOWS_DATA)} workflows")
        
        # ===== RCA METRICS (30 days of data for 5 issues) =====
        print("\n📊 Inserting RCA metrics...")
        rca_count = 0
        issues = ["Payment Failure", "Login Issue", "Shipping Delay", "Wrong Item", "Refund Status"]
        for days_ago in range(30):
            for issue in issues:
                await conn.execute("""
                    INSERT INTO rca_metrics (id, issue_name, date, ticket_count, estimated_cost, created_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """, str(uuid4()), issue, date.today() - timedelta(days=days_ago),
                    random.randint(20, 150), round(random.uniform(500, 5000), 2),
                    datetime.utcnow())
                rca_count += 1
        print(f"✅ Inserted {rca_count} RCA metrics")
        
        # ===== SENTIMENT METRICS (30 days) =====
        print("\n😊 Inserting sentiment metrics...")
        for days_ago in range(30):
            positive = random.randint(40, 60)
            negative = random.randint(10, 25)
            neutral = 100 - positive - negative
            avg_score = round(70 + random.uniform(-10, 20), 1)
            
            await conn.execute("""
                INSERT INTO sentiment_metrics (id, date, average_score, positive_count, negative_count, neutral_count, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, str(uuid4()), date.today() - timedelta(days=days_ago), avg_score,
                positive, negative, neutral, datetime.utcnow())
        print(f"✅ Inserted 30 sentiment metrics")
        
        # ===== VOLUME FORECASTS (7 days: 3 past + 4 future) =====
        print("\n📈 Inserting volume forecasts...")
        for days_offset in range(-3, 4):
            forecast_date = date.today() + timedelta(days=days_offset)
            actual = random.randint(200, 300) if days_offset <= 0 else None
            predicted = random.randint(200, 320)
            
            await conn.execute("""
                INSERT INTO volume_forecasts (id, date, actual_volume, predicted_volume, confidence_score, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, str(uuid4()), forecast_date, actual, predicted, round(random.uniform(0.85, 0.95), 2),
                datetime.utcnow())
        print(f"✅ Inserted 7 volume forecasts")
        
        # ===== AGENT PERFORMANCE =====
        print("\n👥 Inserting agent performance...")
        agents = ["Sarah J.", "Mike T.", "Emma W.", "David L.", "Lisa K.", "John D.", "Amy R.", "Chris P."]
        for agent in agents:
            await conn.execute("""
                INSERT INTO agent_performance (id, agent_name, agent_email, resolved_count, average_resolution_time, csat_score, period_start, period_end, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """, str(uuid4()), agent, f"{agent.lower().replace(' ', '').replace('.', '')}@company.com",
                random.randint(25, 50), round(random.uniform(2.0, 8.0), 1),
                round(random.uniform(4.0, 5.0), 1), date.today() - timedelta(days=30),
                date.today(), datetime.utcnow())
        print(f"✅ Inserted {len(agents)} agent performance records")
        
        # ===== TOPIC CLUSTERS =====
        print("\n🏷️ Inserting topic clusters...")
        for topic in TOPICS_DATA:
            await conn.execute("""
                INSERT INTO topic_clusters (id, topic, volume, trend, keywords, avg_sentiment, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, str(uuid4()), topic["topic"], topic["volume"], topic["trend"],
                json.dumps(topic["keywords"]), topic["avg_sentiment"],
                datetime.utcnow() - timedelta(days=random.randint(30, 90)), datetime.utcnow())
        print(f"✅ Inserted {len(TOPICS_DATA)} topic clusters")
        
        # ===== REGIONAL DATA =====
        print("\n🌍 Inserting regional data...")
        for region in REGIONAL_DATA:
            await conn.execute("""
                INSERT INTO regional_data (id, region, country_code, ticket_volume, avg_sentiment, top_issues, resolution_rate, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """, str(uuid4()), region["region"], region["country_code"], region["volume"],
                region["avg_sentiment"], json.dumps(region["top_issues"]), region["resolution_rate"],
                datetime.utcnow() - timedelta(days=random.randint(30, 90)), datetime.utcnow())
        print(f"✅ Inserted {len(REGIONAL_DATA)} regional data records")
        
        # ===== CHURN PREDICTIONS =====
        print("\n⚠️ Inserting churn predictions...")
        for churn in CHURN_DATA:
            await conn.execute("""
                INSERT INTO churn_predictions (id, customer_segment, risk_score, affected_customers, risk_factors, recommended_actions, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, str(uuid4()), churn["segment"], churn["risk_score"], churn["affected_customers"],
                json.dumps(churn["risk_factors"]), json.dumps(churn["recommended_actions"]),
                datetime.utcnow() - timedelta(days=random.randint(1, 7)), datetime.utcnow())
        print(f"✅ Inserted {len(CHURN_DATA)} churn predictions")
        
        # ===== FRICTION COSTS =====
        print("\n💸 Inserting friction costs...")
        for friction in FRICTION_DATA:
            await conn.execute("""
                INSERT INTO friction_costs (id, friction_point, category, estimated_cost, ticket_count, impact_score, resolution_difficulty, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """, str(uuid4()), friction["friction_point"], friction["category"], friction["cost"],
                friction["ticket_count"], friction["impact_score"], friction["difficulty"],
                datetime.utcnow() - timedelta(days=random.randint(7, 30)), datetime.utcnow())
        print(f"✅ Inserted {len(FRICTION_DATA)} friction cost records")
        
        # ===== STRATEGIC RECOMMENDATIONS =====
        print("\n💡 Inserting strategic recommendations...")
        RECOMMENDATIONS_DATA = [
            {
                "type": "Logistics",
                "title": "Invest in EU Distribution Partner",
                "description": "Shipping delays in Europe are driving 40% of negative sentiment. A local partner could reduce friction cost by $3.2k/week.",
                "impact": "High",
                "confidence": "94%"
            },
            {
                "type": "Product",
                "title": "Fix 'Login Loop' Bug on iOS",
                "description": "Critical cluster 'App Crash' is correlated with the latest iOS update. 150 VIP customers affected.",
                "impact": "Critical",
                "confidence": "98%"
            },
            {
                "type": "Policy",
                "title": "Relax Return Policy for 'Sizing'",
                "description": "Sizing issues have neutral sentiment but high volume. Simplifying returns could boost LTV by 15%.",
                "impact": "Medium",
                "confidence": "85%"
            }
        ]
        for rec in RECOMMENDATIONS_DATA:
            await conn.execute("""
                INSERT INTO strategic_recommendations (id, type, title, description, impact, confidence, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, str(uuid4()), rec["type"], rec["title"], rec["description"], 
                rec["impact"], rec["confidence"], datetime.utcnow(), datetime.utcnow())
        print(f"✅ Inserted {len(RECOMMENDATIONS_DATA)} recommendations")

        print("\n" + "="*60)
        print("✅ ALL DATA POPULATED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  - Policies: {len(POLICIES_DATA)}")
        print(f"  - Workflows: {len(WORKFLOWS_DATA)}")
        print(f"  - RCA Metrics: {rca_count}")
        print(f"  - Sentiment Metrics: 30")
        print(f"  - Volume Forecasts: 7")
        print(f"  - Agent Performance: {len(agents)}")
        print(f"  - Topic Clusters: {len(TOPICS_DATA)}")
        print(f"  - Regional Data: {len(REGIONAL_DATA)}")
        print(f"  - Churn Predictions: {len(CHURN_DATA)}")
        print(f"  - Friction Costs: {len(FRICTION_DATA)}")
        print(f"  - Recommendations: {len(RECOMMENDATIONS_DATA)}")
        total = len(POLICIES_DATA) + len(WORKFLOWS_DATA) + rca_count + 30 + 7 + len(agents) + len(TOPICS_DATA) + len(REGIONAL_DATA) + len(CHURN_DATA) + len(FRICTION_DATA) + len(RECOMMENDATIONS_DATA)
        print(f"\n  TOTAL RECORDS: {total}")
        
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(populate_all_data())
