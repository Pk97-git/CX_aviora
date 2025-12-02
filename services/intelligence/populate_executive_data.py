"""
Populate executive feature tables with initial data.
"""
import asyncio
import asyncpg
import os
from datetime import datetime, timedelta, date
from uuid import uuid4
from decimal import Decimal

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Clean URL for asyncpg
if "sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0] + "?ssl=require"

async def populate_executive_data():
    """Populate executive feature tables"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("🚀 Populating executive feature tables...")
        
        # Clear existing data
        await conn.execute("DELETE FROM financial_metrics")
        await conn.execute("DELETE FROM alert_rules")
        
        # ===== FINANCIAL METRICS (Last 30 days) =====
        print("  💰 Inserting financial metrics...")
        financial_count = 0
        base_revenue = 50000
        base_cost_saved = 15000
        
        for i in range(30):
            day = date.today() - timedelta(days=29-i)
            
            # Add some variation and growth trend
            churn_prevented = 2 + (i % 5)
            revenue_protected = Decimal(base_revenue * (1 + (i * 0.01)) + (i % 7) * 1000)
            automation_saved = Decimal(base_cost_saved * (1 + (i * 0.005)) + (i % 5) * 500)
            friction_reduced = Decimal(8000 + (i % 10) * 800)
            sla_bonus = Decimal(2000 if i % 7 == 0 else 0)
            time_saved = 120 + (i % 15) * 10
            
            total_value = revenue_protected + automation_saved + friction_reduced + sla_bonus
            
            await conn.execute("""
                INSERT INTO financial_metrics (
                    id, date, churn_prevented_count, revenue_protected,
                    automation_cost_saved, resolution_time_saved_hours,
                    friction_cost_reduced, sla_compliance_bonus,
                    total_value_generated, created_at, updated_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """, str(uuid4()), day, churn_prevented, revenue_protected,
                automation_saved, time_saved, friction_reduced, sla_bonus,
                total_value, datetime.utcnow(), datetime.utcnow())
            financial_count += 1
        
        print(f"  ✅ Inserted {financial_count} financial metrics")
        
        # ===== ALERT RULES =====
        print("  🚨 Inserting alert rules...")
        ALERT_RULES = [
            {
                "name": "SLA Breach Alert",
                "metric_type": "sla_breach",
                "threshold_value": 5.0,  # More than 5 tickets at risk
                "severity": "critical",
                "notification_channels": ["email", "slack"]
            },
            {
                "name": "High Churn Risk",
                "metric_type": "churn_risk",
                "threshold_value": 10.0,  # More than 10 at-risk customers
                "severity": "high",
                "notification_channels": ["email"]
            },
            {
                "name": "Sentiment Drop",
                "metric_type": "sentiment_drop",
                "threshold_value": -15.0,  # 15% drop in positive sentiment
                "severity": "high",
                "notification_channels": ["email", "slack"]
            },
            {
                "name": "Volume Spike",
                "metric_type": "volume_spike",
                "threshold_value": 200.0,  # More than 200 tickets/day
                "severity": "medium",
                "notification_channels": ["email"]
            }
        ]
        
        for rule in ALERT_RULES:
            await conn.execute("""
                INSERT INTO alert_rules (
                    id, name, metric_type, threshold_value, severity,
                    notification_channels, enabled, created_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, str(uuid4()), rule["name"], rule["metric_type"],
                rule["threshold_value"], rule["severity"],
                rule["notification_channels"], True, datetime.utcnow())
        
        print(f"  ✅ Inserted {len(ALERT_RULES)} alert rules")
        
        print("\n✅ Executive feature data populated successfully!")
        print(f"\n📊 Summary:")
        print(f"  - Financial Metrics: {financial_count} days")
        print(f"  - Alert Rules: {len(ALERT_RULES)}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(populate_executive_data())
