import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv('services/intelligence/.env')

async def check_ticket():
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    result = await conn.fetchrow(
        "SELECT id, subject, sentiment, intent, urgency, category, ai_summary FROM tickets WHERE id = $1",
        "final-test-001"
    )
    
    await conn.close()
    
    if result:
        print(f"✅ Ticket Found: {result['id'][:8]}")
        print(f"Subject: {result['subject']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Intent: {result['intent']}")
        print(f"Urgency: {result['urgency']}")
        print(f"Category: {result['category']}")
        print(f"AI Summary: {result['ai_summary']}")
        
        if result['sentiment'] and result['intent']:
            print("\n✅ VERIFICATION SUCCESS: AI analysis completed!")
        else:
            print("\n⚠️  Ticket exists but AI analysis pending...")
    else:
        print("❌ Ticket not found in database")

asyncio.run(check_ticket())
