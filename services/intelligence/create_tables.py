"""
Create database tables using SQLAlchemy models.
Run this script to initialize the Neon database with required tables.
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Base and models
from app.core.database import Base, database_url
from app.models.database import Ticket, AIAnalysis

async def create_tables():
    """Create all tables defined in SQLAlchemy models."""
    print(f"Connecting to database...")
    print(f"Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'unknown'}")
    
    # Create async engine
    from app.core.database import engine
    
    print("Creating tables...")
    async with engine.begin() as conn:
        # Drop all tables (use with caution!)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Tables created successfully!")
    
    # Verify tables exist
    async with engine.connect() as conn:
        from sqlalchemy import text
        result = await conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        print(f"\nTables in database: {tables}")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())
