import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.database import Base
from app.models.strategy import StrategicRecommendation

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
engine = create_async_engine(DATABASE_URL, echo=True)

async def create_table():
    """Create strategic_recommendations table"""
    print("🚀 Creating strategic_recommendations table...")
    
    async with engine.begin() as conn:
        # Create specific table
        await conn.run_sync(StrategicRecommendation.__table__.create)
    
    print("✅ Table created successfully!")

if __name__ == "__main__":
    asyncio.run(create_table())
