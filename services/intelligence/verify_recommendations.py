import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.api.routes.strategy import get_strategic_recommendations

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Clean URL for asyncpg
if "sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0] + "?ssl=require"

# Ensure asyncpg protocol for SQLAlchemy
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create engine
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def verify_api():
    """Verify the API endpoint logic"""
    print("🚀 Verifying get_strategic_recommendations API logic...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Call the API function directly
            recommendations = await get_strategic_recommendations(db=session)
            
            print(f"✅ API returned {len(recommendations)} recommendations")
            for rec in recommendations:
                print(f"  - [{rec.type}] {rec.title} (Impact: {rec.impact})")
                
            if len(recommendations) > 0:
                print("\n🎉 VERIFICATION SUCCESSFUL: API is correctly fetching from DB!")
            else:
                print("\n❌ VERIFICATION FAILED: No data returned.")
                
        except Exception as e:
            print(f"\n❌ VERIFICATION FAILED: {str(e)}")

if __name__ == "__main__":
    asyncio.run(verify_api())
