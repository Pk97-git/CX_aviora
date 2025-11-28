"""
Execute SQL file directly using asyncpg.
"""
import asyncio
import asyncpg
import os

async def run_sql():
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    
    # Clean URL for asyncpg
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgres://', 1)
    
    # Remove sslmode and channel_binding
    database_url = database_url.replace('sslmode=require', '').replace('channel_binding=require', '')
    database_url = database_url.replace('?&', '?').replace('&&', '&')
    if database_url.endswith('?') or database_url.endswith('&'):
        database_url = database_url[:-1]
    
    print(f"🔌 Connecting to database...")
    
    # Connect directly with asyncpg
    conn = await asyncpg.connect(database_url, ssl='require')
    
    print("📖 Reading SQL file...")
    with open('/app/mock_data.sql', 'r') as f:
        sql = f.read()
    
    print("🚀 Executing SQL...")
    
    # Split by semicolons and execute each statement
    statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]
    
    for i, stmt in enumerate(statements):
        if stmt:
            try:
                result = await conn.fetch(stmt)
                if result:
                    print(f"✅ Statement {i+1}: {result}")
            except Exception as e:
                print(f"⚠️  Statement {i+1} error: {e}")
    
    await conn.close()
    print("\n🎉 Mock data loaded successfully!")

if __name__ == "__main__":
    asyncio.run(run_sql())
