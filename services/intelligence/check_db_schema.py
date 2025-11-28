"""
Check existing database schema and create missing tables.
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()

async def check_and_create():
    # Get database URL
    from app.core.database import database_url
    
    print(f"Connecting to database...")
    
    # Create engine
    from app.core.database import engine
    
    async with engine.connect() as conn:
        # Check existing tables
        result = await conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        print(f"\nExisting tables: {tables}")
        
        # Check tickets table schema
        if 'tickets' in tables:
            result = await conn.execute(text("""
                SELECT column_name, data_type, udt_name
                FROM information_schema.columns 
                WHERE table_name='tickets' 
                ORDER BY ordinal_position
            """))
            print(f"\nTickets table schema:")
            for row in result:
                print(f"  {row[0]}: {row[1]} ({row[2]})")
        
        # Create ai_analysis table if it doesn't exist
        if 'ai_analysis' not in tables:
            print(f"\nCreating ai_analysis table...")
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ai_analysis (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    ticket_id UUID NOT NULL REFERENCES tickets(id),
                    sentiment FLOAT,
                    intent VARCHAR(255),
                    urgency VARCHAR(50),
                    category VARCHAR(255),
                    priority_score FLOAT,
                    summary TEXT,
                    suggested_actions JSONB,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
            await conn.commit()
            print("✅ ai_analysis table created!")
        else:
            print(f"\n✅ ai_analysis table already exists")
    
    await engine.dispose()
    print(f"\n✅ Database check complete!")

if __name__ == "__main__":
    asyncio.run(check_and_create())
