import asyncio
import asyncpg
import os
from datetime import datetime
from uuid import uuid4

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Clean URL for asyncpg
if "sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0] + "?ssl=require"

# NOTE: asyncpg.connect() expects 'postgresql://', NOT 'postgresql+asyncpg://'
# So we do NOT replace the protocol here.

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

async def populate_recommendations():
    """Populate strategic recommendations table"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("🚀 Populating strategic recommendations...")
        
        for rec in RECOMMENDATIONS_DATA:
            await conn.execute("""
                INSERT INTO strategic_recommendations (id, type, title, description, impact, confidence, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, str(uuid4()), rec["type"], rec["title"], rec["description"], 
                rec["impact"], rec["confidence"], datetime.utcnow(), datetime.utcnow())
            
        print(f"✅ Inserted {len(RECOMMENDATIONS_DATA)} recommendations")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(populate_recommendations())
