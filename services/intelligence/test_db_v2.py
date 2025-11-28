import asyncio
import os
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

# Raw URL
raw_url = os.getenv("DATABASE_URL", "")
print(f"RAW: {raw_url}")

# Process
url = raw_url
if url.startswith("postgresql://"):
    url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove params
for param in ["sslmode", "channel_binding"]:
    for mode in ["require", "prefer", "disable"]:
        url = url.replace(f"{param}={mode}", "")

# Clean up
url = url.replace("?&", "?").replace("&&", "&")
if url.endswith("?") or url.endswith("&"):
    url = url[:-1]

# Add ssl
if "ssl=" not in url:
    sep = "&" if "?" in url else "?"
    url += f"{sep}ssl=require"

print(f"CLEAN: {url}")

async def test():
    # Test 1: asyncpg direct
    print("\n--- Testing asyncpg direct ---")
    try:
        # asyncpg expects postgresql:// not postgresql+asyncpg://
        pg_url = url.replace("postgresql+asyncpg://", "postgresql://")
        print(f"Connecting to: {pg_url.split('@')[1] if '@' in pg_url else '...'}")
        conn = await asyncpg.connect(pg_url)
        print("✅ asyncpg success")
        await conn.close()
    except Exception as e:
        print(f"❌ asyncpg failed: {e}")

    # Test 2: SQLAlchemy
    print("\n--- Testing SQLAlchemy ---")
    try:
        print(f"Connecting to: {url.split('@')[1] if '@' in url else '...'}")
        engine = create_async_engine(url)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ SQLAlchemy success")
        await engine.dispose()
    except Exception as e:
        print(f"❌ SQLAlchemy failed: {e}")

if __name__ == "__main__":
    asyncio.run(test())
