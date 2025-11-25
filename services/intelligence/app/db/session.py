from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

# Create async engine
# Note: DATABASE_URL must start with postgresql+asyncpg://
database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
# asyncpg doesn't support sslmode in URL, so we strip it
if "?" in database_url:
    database_url = database_url.split("?")[0]

engine = create_async_engine(
    database_url, 
    echo=False, 
    future=True,
    connect_args={"ssl": "require"}
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
