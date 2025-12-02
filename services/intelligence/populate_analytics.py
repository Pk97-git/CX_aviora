"""
Populate analytics tables with initial data.
"""
import asyncio
import asyncpg
import os
from datetime import datetime, timedelta, date
from uuid import uuid4

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Clean URL for asyncpg
if "sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0] + "?ssl=require"

# RCA Data
RCA_DATA = [
    {"category": "Shipping Delays", "ticket_count": 245, "avg_resolution_hours": 18.5, "severity": "high"},
    {"category": "Product Defects", "ticket_count": 189, "avg_resolution_hours": 24.2, "severity": "high"},
    {"category": "Login Issues", "ticket_count": 156, "avg_resolution_hours": 4.5, "severity": "medium"},
    {"category": "Payment Failures", "ticket_count": 134, "avg_resolution_hours": 6.8, "severity": "high"},
    {"category": "Account Access", "ticket_count": 98, "avg_resolution_hours": 12.3, "severity": "medium"},
    {"category": "Sizing Problems", "ticket_count": 87, "avg_resolution_hours": 15.7, "severity": "low"},
    {"category": "Return Policy", "ticket_count": 76, "avg_resolution_hours": 8.2, "severity": "low"},
    {"category": "App Crashes", "ticket_count": 65, "avg_resolution_hours": 16.4, "severity": "high"},
]

async def populate_analytics():
    """Populate analytics tables"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("🚀 Populating analytics tables...")
        
        # Clear existing data
        await conn.execute("DELETE FROM rca_metrics")
        await conn.execute("DELETE FROM sentiment_metrics")
        await conn.execute("DELETE FROM volume_forecasts")
        
        # Insert RCA metrics
        print("  📊 Inserting RCA metrics...")
        for rca in RCA_DATA:
            await conn.execute("""
                INSERT INTO rca_metrics (id, category, ticket_count, avg_resolution_hours, severity, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, str(uuid4()), rca["category"], rca["ticket_count"], 
                rca["avg_resolution_hours"], rca["severity"], 
                datetime.utcnow(), datetime.utcnow())
        print(f"  ✅ Inserted {len(RCA_DATA)} RCA metrics")
        
        # Insert sentiment metrics (last 30 days)
        print("  📊 Inserting sentiment metrics...")
        sentiment_count = 0
        for i in range(30):
            day = date.today() - timedelta(days=29-i)
            # Vary sentiment over time
            positive = 45 + (i % 10) * 2
            negative = 20 + (i % 7) * 2
            neutral = 100 - positive - negative
            
            await conn.execute("""
                INSERT INTO sentiment_metrics (id, date, positive, neutral, negative, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, str(uuid4()), day, positive, neutral, negative, 
                datetime.utcnow(), datetime.utcnow())
            sentiment_count += 1
        print(f"  ✅ Inserted {sentiment_count} sentiment metrics")
        
        # Insert volume forecasts (next 30 days)
        print("  📊 Inserting volume forecasts...")
        forecast_count = 0
        base_volume = 120
        for i in range(30):
            day = date.today() + timedelta(days=i)
            # Add some variation and growth trend
            predicted = int(base_volume * (1 + (i * 0.01)) + (i % 7) * 5)
            lower = int(predicted * 0.8)
            upper = int(predicted * 1.2)
            # Only past 5 days have actual data
            actual = predicted - 10 + (i % 5) * 4 if i < 5 else None
            
            await conn.execute("""
                INSERT INTO volume_forecasts (id, date, actual, predicted, lower_bound, upper_bound, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, str(uuid4()), day, actual, predicted, lower, upper, 
                datetime.utcnow(), datetime.utcnow())
            forecast_count += 1
        print(f"  ✅ Inserted {forecast_count} volume forecasts")
        
        print("\n✅ Analytics data populated successfully!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(populate_analytics())
