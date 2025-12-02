"""
Create analytics tables in the database.
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.database import Base
from app.models.analytics import RCAMetric, SentimentMetric, VolumeForecast

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
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

async def create_tables():
    """Create analytics tables"""
    print("🚀 Creating analytics tables...")
    
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(RCAMetric.__table__.create, checkfirst=True)
        await conn.run_sync(SentimentMetric.__table__.create, checkfirst=True)
        await conn.run_sync(VolumeForecast.__table__.create, checkfirst=True)
    
    print("✅ Analytics tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
