"""
Populate alerts table with mock data for testing
"""
import asyncio
import asyncpg
import os
from datetime import datetime, timedelta

async def populate_alerts():
    DATABASE_URL = os.getenv("DATABASE_URL", "").replace("postgresql://", "postgresql+asyncpg://")
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    # Use asyncpg directly
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Clear existing alerts
        await conn.execute("DELETE FROM alerts WHERE id > 0")
        print("✓ Cleared existing alerts")
        
        # Create mock alerts
        alerts = [
            {
                "rule_id": "rule_001",
                "rule_name": "High SLA Breach Rate",
                "severity": "critical",
                "message": "SLA breach rate has exceeded 15% in the last hour. Immediate action required.",
                "triggered_at": datetime.utcnow() - timedelta(minutes=30),
                "acknowledged": False,
                "metadata": {"breach_rate": 18.5, "threshold": 15.0}
            },
            {
                "rule_id": "rule_002",
                "rule_name": "Churn Risk Alert",
                "severity": "high",
                "message": "5 high-value customers showing churn indicators in the past 24 hours.",
                "triggered_at": datetime.utcnow() - timedelta(hours=2),
                "acknowledged": False,
                "metadata": {"at_risk_customers": 5, "total_value": 125000}
            },
            {
                "rule_id": "rule_003",
                "rule_name": "Sentiment Drop Detected",
                "severity": "medium",
                "message": "Average sentiment score dropped from 0.75 to 0.62 in the last 6 hours.",
                "triggered_at": datetime.utcnow() - timedelta(hours=4),
                "acknowledged": False,
                "metadata": {"previous_score": 0.75, "current_score": 0.62}
            },
            {
                "rule_id": "rule_004",
                "rule_name": "Volume Spike",
                "severity": "medium",
                "message": "Ticket volume increased by 45% compared to the same time last week.",
                "triggered_at": datetime.utcnow() - timedelta(hours=1),
                "acknowledged": False,
                "metadata": {"current_volume": 145, "expected_volume": 100}
            }
        ]
        
        for alert in alerts:
            await conn.execute("""
                INSERT INTO alerts (
                    rule_id, rule_name, severity, message, 
                    triggered_at, acknowledged, metadata
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, 
                alert["rule_id"],
                alert["rule_name"],
                alert["severity"],
                alert["message"],
                alert["triggered_at"],
                alert["acknowledged"],
                str(alert["metadata"])  # Convert dict to string
            )
        
        print(f"✓ Created {len(alerts)} mock alerts")
        
        # Verify
        count = await conn.fetchval("SELECT COUNT(*) FROM alerts WHERE acknowledged = false")
        print(f"✓ Total active alerts: {count}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(populate_alerts())
