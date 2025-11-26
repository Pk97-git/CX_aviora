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
    version="1.0.0",
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
        "https://cx-aviora-fecaitvzg-prashanths-projects-626ff807.vercel.app",  # Vercel production
        "https://*.vercel.app",   # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
from app.api.routes import tickets, analytics, strategy

app.include_router(tickets.router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(strategy.router, prefix="/api/strategy", tags=["Strategy"])

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
