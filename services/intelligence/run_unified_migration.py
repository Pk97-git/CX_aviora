"""
Script to run unified schema migration
"""
import asyncio
import asyncpg
import os

async def run_migration():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:***REMOVED***@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
    
    # Convert asyncpg URL format
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Read migration SQL
        with open('migrations/003_unified_schema.sql', 'r') as f:
            sql = f.read()
        
        # Execute migration
        await conn.execute(sql)
        print("✓ Unified schema migration completed successfully")
        print("✓ All Phase 1-3 tables created/updated")
        print("✓ Old ai_analysis table dropped")
        
    except Exception as e:
        print(f"✗ Error running migration: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run_migration())
