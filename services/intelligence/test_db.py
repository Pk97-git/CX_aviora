import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

# Get database URL from env or use a default (placeholder)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_6s8LwzXlQhWe@ep-young-snow-a1h4us5d-pooler.ap-southeast-1.aws.neon.tech/neondb")

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove sslmode and channel_binding if present
if "sslmode=" in DATABASE_URL or "channel_binding=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("sslmode=require", "")
    DATABASE_URL = DATABASE_URL.replace("sslmode=prefer", "")
    DATABASE_URL = DATABASE_URL.replace("sslmode=disable", "")
    DATABASE_URL = DATABASE_URL.replace("channel_binding=require", "")
    DATABASE_URL = DATABASE_URL.replace("channel_binding=prefer", "")
    DATABASE_URL = DATABASE_URL.replace("channel_binding=disable", "")
    
    DATABASE_URL = DATABASE_URL.replace("?&", "?").replace("&&", "&")
    if DATABASE_URL.endswith("?") or DATABASE_URL.endswith("&"):
        DATABASE_URL = DATABASE_URL[:-1]

if "ssl=" not in DATABASE_URL:
    separator = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL += f"{separator}ssl=require"

async def test_db():
    print(f"Connecting to {DATABASE_URL.split('@')[1]}...")
    try:
        # Match app/core/database.py config
        engine = create_async_engine(
            DATABASE_URL, 
            echo=True
        )
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"Connection successful! Result: {result.scalar()}")
            
            # Test tickets query
            print("Testing tickets query...")
            result = await conn.execute(text("SELECT count(*) FROM tickets"))
            count = result.scalar()
            print(f"Found {count} tickets")
            
            # Test join query
            print("Testing join query...")
            result = await conn.execute(text("SELECT t.id, a.sentiment FROM tickets t LEFT JOIN ai_analysis a ON t.id = a.ticket_id LIMIT 1"))
            row = result.first()
            print(f"Join successful! Row: {row}")
            
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_db())
