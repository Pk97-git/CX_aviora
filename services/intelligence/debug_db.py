import asyncio
import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("DATABASE_URL", "")
# Clean up URL
if BASE_URL.startswith("postgresql://"):
    BASE_URL = BASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove params for clean slate
if "?" in BASE_URL:
    BASE_URL = BASE_URL.split("?")[0]

async def try_connect(name, url, connect_args=None):
    print(f"\n--- Testing {name} ---")
    print(f"URL: {url}")
    print(f"Args: {connect_args}")
    try:
        engine = create_async_engine(url, connect_args=connect_args or {}, echo=False)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"✅ SUCCESS! Result: {result.scalar()}")
            return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    finally:
        await engine.dispose()

async def main():
    # Method 1: URL param ?ssl=require
    url1 = f"{BASE_URL}?ssl=require"
    await try_connect("Method 1 (URL ?ssl=require)", url1)

    # Method 2: connect_args={"ssl": "require"}
    await try_connect("Method 2 (connect_args='require')", BASE_URL, {"ssl": "require"})

    # Method 3: connect_args={"ssl": True}
    # Note: asyncpg might not support True directly for ssl param if it expects string or context
    # await try_connect("Method 3 (connect_args=True)", BASE_URL, {"ssl": True})

    # Method 4: SSL Context
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    await try_connect("Method 4 (SSL Context - No Verify)", BASE_URL, {"ssl": ctx})

if __name__ == "__main__":
    asyncio.run(main())
