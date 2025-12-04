"""
Script to create ticket tables in the database
"""
import asyncio
import asyncpg
import os

async def create_tables():
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Read migration SQL
        with open('migrations/002_add_tickets.sql', 'r') as f:
            sql = f.read()
        
        # Execute migration
        await conn.execute(sql)
        print("✓ Ticket tables created successfully")
        
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_tables())
