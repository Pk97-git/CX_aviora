import asyncio
from sqlalchemy import text
from app.core.database import engine

async def check():
    async with engine.begin() as conn:
        result = await conn.execute(text('SELECT COUNT(*) FROM tickets'))
        count = result.scalar()
        print(f'✅ Tickets in database: {count}')
        
        result2 = await conn.execute(text('SELECT COUNT(*) FROM ai_analysis'))
        count2 = result2.scalar()
        print(f'✅ AI Analyses in database: {count2}')
        
        if count > 0:
            sample = await conn.execute(text('SELECT id, title, status, priority FROM tickets LIMIT 3'))
            print(f'\n📋 Sample tickets:')
            for row in sample:
                print(f"  - {row.title} ({row.status}, {row.priority})")

asyncio.run(check())
