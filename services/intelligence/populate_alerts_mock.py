"""
Populate alerts table with mock data for testing
"""
import asyncio
import asyncpg
import os
import uuid
from datetime import datetime, timedelta

async def populate_alerts():
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    # Use asyncpg directly
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Clear existing alerts
        await conn.execute("DELETE FROM alerts WHERE id IS NOT NULL")
        print("✓ Cleared existing alerts")
        
        # Create mock alerts matching the actual schema
        alerts = [
            {
                "id": str(uuid.uuid4()),
                "rule_id": "rule_001",
                "alert_type": "sla_breach",
                "severity": "critical",
                "title": "High SLA Breach Rate",
                "message": "SLA breach rate has exceeded 15% in the last hour. Immediate action required.",
                "metric_value": 18.5,
                "triggered_at": datetime.utcnow() - timedelta(minutes=30),
                "acknowledged_at": None,
                "acknowledged_by": None
            },
            {
                "id": str(uuid.uuid4()),
                "rule_id": "rule_002",
                "alert_type": "churn_risk",
                "severity": "high",
                "title": "Churn Risk Alert",
                "message": "5 high-value customers showing churn indicators in the past 24 hours.",
                "metric_value": 5.0,
                "triggered_at": datetime.utcnow() - timedelta(hours=2),
                "acknowledged_at": None,
                "acknowledged_by": None
            },
            {
                "id": str(uuid.uuid4()),
                "rule_id": "rule_003",
                "alert_type": "sentiment_drop",
                "severity": "medium",
                "title": "Sentiment Drop Detected",
                "message": "Average sentiment score dropped from 0.75 to 0.62 in the last 6 hours.",
                "metric_value": 0.62,
                "triggered_at": datetime.utcnow() - timedelta(hours=4),
                "acknowledged_at": None,
                "acknowledged_by": None
            },
            {
                "id": str(uuid.uuid4()),
                "rule_id": "rule_004",
                "alert_type": "volume_spike",
                "severity": "medium",
                "title": "Volume Spike",
                "message": "Ticket volume increased by 45% compared to the same time last week.",
                "metric_value": 145.0,
                "triggered_at": datetime.utcnow() - timedelta(hours=1),
                "acknowledged_at": None,
                "acknowledged_by": None
            }
        ]
        
        for alert in alerts:
            await conn.execute("""
                INSERT INTO alerts (
                    id, rule_id, alert_type, severity, title, message,
                    metric_value, triggered_at, acknowledged_at, acknowledged_by
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            """, 
                alert["id"],
                alert["rule_id"],
                alert["alert_type"],
                alert["severity"],
                alert["title"],
                alert["message"],
                alert["metric_value"],
                alert["triggered_at"],
                alert["acknowledged_at"],
                alert["acknowledged_by"]
            )
        
        print(f"✓ Created {len(alerts)} mock alerts")
        
        # Verify
        count = await conn.fetchval("SELECT COUNT(*) FROM alerts WHERE acknowledged_at IS NULL")
        print(f"✓ Total active alerts: {count}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(populate_alerts())
