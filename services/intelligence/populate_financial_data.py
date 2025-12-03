"""
Populate all financial tables with realistic mock data
"""
import asyncio
import asyncpg
import os
import uuid
import json
from datetime import datetime, date, timedelta
from decimal import Decimal

async def populate_financial_data():
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Clear existing data
        await conn.execute("DELETE FROM financial_metrics WHERE id IS NOT NULL")
        await conn.execute("DELETE FROM roi_calculations WHERE id IS NOT NULL")
        print("✓ Cleared existing financial data")
        
        # Create financial metrics for the last 30 days
        today = date.today()
        for i in range(30):
            metric_date = today - timedelta(days=29-i)
            
            # Realistic daily values
            churn_prevented = 3 + (i % 5)
            revenue_protected = Decimal(churn_prevented * 15000)  # $15k per customer
            automation_saved = Decimal(2500 + (i * 100))
            time_saved = 8.5 + (i * 0.2)
            friction_reduced = Decimal(1200 + (i * 50))
            sla_bonus = Decimal(500 if i % 3 == 0 else 0)
            
            total_value = revenue_protected + automation_saved + friction_reduced + sla_bonus
            
            await conn.execute("""
                INSERT INTO financial_metrics (
                    id, date, churn_prevented_count, revenue_protected,
                    automation_cost_saved, resolution_time_saved_hours,
                    friction_cost_reduced, sla_compliance_bonus,
                    total_value_generated, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            """,
                str(uuid.uuid4()),
                metric_date,
                churn_prevented,
                revenue_protected,
                automation_saved,
                time_saved,
                friction_reduced,
                sla_bonus,
                total_value,
                datetime.utcnow()
            )
        
        print(f"✓ Created 30 days of financial metrics")
        
        # Create ROI calculation for last 30 days
        period_start = today - timedelta(days=29)
        period_end = today
        
        # Calculate totals
        total_investment = Decimal(10000)  # Platform cost
        total_return = Decimal(2673125)  # Sum of all value generated
        roi_percentage = float((total_return - total_investment) / total_investment * 100)
        payback_months = float(total_investment / (total_return / 30) * 30 / 365 * 12)
        
        breakdown_data = {
            "automation_savings": 75000,
            "churn_prevention": 1802500,
            "friction_reduction": 36000,
            "sla_compliance": 15000,
            "efficiency_gains": 744625
        }
        
        await conn.execute("""
            INSERT INTO roi_calculations (
                id, period_start, period_end, total_investment,
                total_return, roi_percentage, breakdown, calculated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """,
            str(uuid.uuid4()),
            period_start,
            period_end,
            total_investment,
            total_return,
            roi_percentage,
            json.dumps(breakdown_data),  # Properly serialize as JSON
            datetime.utcnow()
        )
        
        print(f"✓ Created ROI calculation")
        print(f"  - ROI: {roi_percentage:.1f}%")
        print(f"  - Payback: {payback_months:.1f} months")
        
        # Verify
        metrics_count = await conn.fetchval("SELECT COUNT(*) FROM financial_metrics")
        roi_count = await conn.fetchval("SELECT COUNT(*) FROM roi_calculations")
        print(f"✓ Total financial metrics: {metrics_count}")
        print(f"✓ Total ROI calculations: {roi_count}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(populate_financial_data())
