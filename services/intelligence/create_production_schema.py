"""
Create all production database tables.
"""
import asyncio
from app.core.database import engine, Base
from app.models.database import Ticket, AIAnalysis
from app.models.policies import Policy
from app.models.workflows import Workflow
from app.models.analytics import RCAMetric, SentimentMetric, VolumeForecast, AgentPerformance
from app.models.strategy import TopicCluster, RegionalData, ChurnPrediction, FrictionCost


async def create_tables():
    """Create all database tables"""
    print("🚀 Creating production database schema...")
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ All tables created successfully!")
    print("\nCreated tables:")
    print("  - tickets (existing)")
    print("  - ai_analysis (existing)")
    print("  - policies (new)")
    print("  - workflows (new)")
    print("  - rca_metrics (new)")
    print("  - sentiment_metrics (new)")
    print("  - volume_forecasts (new)")
    print("  - agent_performance (new)")
    print("  - topic_clusters (new)")
    print("  - regional_data (new)")
    print("  - churn_predictions (new)")
    print("  - friction_costs (new)")


if __name__ == "__main__":
    asyncio.run(create_tables())
