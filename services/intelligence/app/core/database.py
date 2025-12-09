"""
Database connection and session management.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

# Convert DATABASE_URL to async format if needed
database_url = settings.DATABASE_URL

# Fix protocol
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)

# Remove sslmode and channel_binding if present (asyncpg doesn't support them)
if "sslmode=" in database_url or "channel_binding=" in database_url:
    database_url = database_url.replace("sslmode=require", "")
    database_url = database_url.replace("sslmode=prefer", "")
    database_url = database_url.replace("sslmode=disable", "")
    database_url = database_url.replace("channel_binding=require", "")
    database_url = database_url.replace("channel_binding=prefer", "")
    database_url = database_url.replace("channel_binding=disable", "")
    
    # Clean up potential double && or trailing ?
    database_url = database_url.replace("?&", "?").replace("&&", "&")
    if database_url.endswith("?") or database_url.endswith("&"):
        database_url = database_url[:-1]

# Ensure ssl=require is present for Neon
if "ssl=" not in database_url:
    separator = "&" if "?" in database_url else "?"
    database_url += f"{separator}ssl=require"

# Debug: Print the final URL (remove in production)
print(f"[DEBUG] Final DATABASE_URL: {database_url.split('@')[1] if '@' in database_url else 'invalid'}")

# Create async engine
engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Import Base from models (don't create duplicate)
from app.models.database import Base


async def init_db():
    """
    Initialize database tables.
    """
    # Import all models so Base.metadata knows about them
    from app.models.tenant import Tenant, User, APIKey, Integration
    from app.models.ticket import Ticket, TicketComment, AIAnalysis
    from app.models.executive import FinancialMetric, ROICalculation, AlertRule, Alert, SavedReport, ReportDelivery
    from app.models.strategy import ChurnPrediction, FeatureRequest, CompetitorAnalysis, MarketTrend
    from app.models.analytics import TicketMetric, AgentPerformance, SentimentMetric
    from app.models.workflow import Workflow, WorkflowExecution, WorkflowLog
    from app.models.policy import Policy, PolicyVersion, ComplianceCheck, AuditLog
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")


async def get_db() -> AsyncSession:
    """
    Dependency to get database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
