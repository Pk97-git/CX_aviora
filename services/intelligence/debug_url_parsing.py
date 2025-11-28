import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url

load_dotenv()

raw_url = os.getenv("DATABASE_URL", "")
print(f"RAW URL: {raw_url}")

# Simulate app/core/database.py logic
database_url = raw_url
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

if "sslmode=" in database_url or "channel_binding=" in database_url:
    database_url = database_url.replace("sslmode=require", "")
    database_url = database_url.replace("sslmode=prefer", "")
    database_url = database_url.replace("sslmode=disable", "")
    database_url = database_url.replace("channel_binding=require", "")
    database_url = database_url.replace("channel_binding=prefer", "")
    database_url = database_url.replace("channel_binding=disable", "")
    
    database_url = database_url.replace("?&", "?").replace("&&", "&")
    if database_url.endswith("?") or database_url.endswith("&"):
        database_url = database_url[:-1]

if "ssl=" not in database_url:
    separator = "&" if "?" in database_url else "?"
    database_url += f"{separator}ssl=require"

print(f"PROCESSED URL: {database_url}")

# Parse with make_url to see what SQLAlchemy sees
try:
    u = make_url(database_url)
    print(f"Parsed Query: {u.query}")
except Exception as e:
    print(f"Parsing Error: {e}")
