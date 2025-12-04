from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.core.config import get_settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Intelligence Service starting up...")
    
    # Start Redis Consumer in background
    import asyncio
    from app.consumers.redis_consumer import redis_consumer
    
    task = asyncio.create_task(redis_consumer.start())
    
    yield
    
    logger.info("Intelligence Service shutting down...")
    await redis_consumer.stop()
    await task

app = FastAPI(
    title="Aivora Intelligence Service",
    description="AI-powered customer support intelligence and analytics",
    version="1.1.0",  # Bumped to trigger deployment
    lifespan=lifespan
)

# CORS Configuration
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Vite dev server
        "http://localhost:5173",  # Alternative Vite port
        "https://*.render.com",   # Render deployments
        "https://cx-aviora.vercel.app",  # Vercel production (new URL)
        "https://cx-aviora-fecaitvzg-prashanths-projects-626ff807.vercel.app",  # Vercel production (old URL)
        "https://*.vercel.app",   # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Tenant Context Middleware
from app.middleware.tenant import TenantContextMiddleware
app.add_middleware(TenantContextMiddleware)

# Register API Routers
from app.api.routes import tickets, analytics, strategy, workflows, policies, admin, financial, alerts, auth, admin_users

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(admin_users.router, prefix="/api/admin", tags=["Admin"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(strategy.router, prefix="/api/strategy", tags=["Strategy"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["Workflows"])
app.include_router(policies.router, prefix="/api/policies", tags=["Policies"])
app.include_router(financial.router, prefix="/api/financial", tags=["Financial"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(admin.router, tags=["Admin"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "intelligence", "version": "1.0.0"}

# Debug Endpoint
@app.get("/debug")
async def debug_status():
    settings = get_settings()
    redis_status = "unknown"
    
    # Check Redis
    try:
        from app.core.redis import redis_client
        if await redis_client.ping():
            redis_status = "connected"
        else:
            redis_status = "failed"
    except Exception as e:
        redis_status = f"error: {str(e)}"
    
    return {
        "status": "debug",
        "redis": redis_status,
        "env_vars": {
            "has_redis_url": bool(settings.REDIS_URL),
            "has_db_url": bool(settings.DATABASE_URL),
            "has_groq_key": bool(settings.GROQ_API_KEY)
        }
    }
