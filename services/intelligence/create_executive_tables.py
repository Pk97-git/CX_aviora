"""
Create executive feature tables in the database.
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.database import Base
from app.models.executive import (
    FinancialMetric,
    ROICalculation,
    AlertRule,
    Alert,
    SavedReport,
    ReportDelivery
)

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
    """Create executive feature tables"""
    print("🚀 Creating executive feature tables...")
    
    async with engine.begin() as conn:
        # Drop existing tables to ensure clean schema
        print("  🗑️ Dropping existing executive tables...")
        await conn.run_sync(FinancialMetric.__table__.drop, checkfirst=True)
        await conn.run_sync(ROICalculation.__table__.drop, checkfirst=True)
        await conn.run_sync(AlertRule.__table__.drop, checkfirst=True)
        await conn.run_sync(Alert.__table__.drop, checkfirst=True)
        await conn.run_sync(SavedReport.__table__.drop, checkfirst=True)
        await conn.run_sync(ReportDelivery.__table__.drop, checkfirst=True)

        # Create tables
        print("  ✨ Creating new executive tables...")
        await conn.run_sync(FinancialMetric.__table__.create, checkfirst=True)
        await conn.run_sync(ROICalculation.__table__.create, checkfirst=True)
        await conn.run_sync(AlertRule.__table__.create, checkfirst=True)
        await conn.run_sync(Alert.__table__.create, checkfirst=True)
        await conn.run_sync(SavedReport.__table__.create, checkfirst=True)
        await conn.run_sync(ReportDelivery.__table__.create, checkfirst=True)
    
    print("✅ Executive feature tables created successfully!")
    print("   - financial_metrics")
    print("   - roi_calculations")
    print("   - alert_rules")
    print("   - alerts")
    print("   - saved_reports")
    print("   - report_deliveries")

if __name__ == "__main__":
    asyncio.run(create_tables())
