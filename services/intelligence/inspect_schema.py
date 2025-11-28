import asyncio
import asyncpg
import os

async def inspect_schema():
    # Get and clean DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    db_url = db_url.replace('postgresql://', 'postgres://')
    db_url = db_url.replace('sslmode=require', '').replace('channel_binding=require', '')
    db_url = db_url.replace('?&', '?').replace('&&', '&')
    if db_url.endswith('?') or db_url.endswith('&'):
        db_url = db_url[:-1]
    
    print("Connecting to database...")
    conn = await asyncpg.connect(db_url, ssl='require')
    
    output = []
    output.append("\n=== TICKETS TABLE ===")
    rows = await conn.fetch("""
        SELECT column_name, data_type, udt_name, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'tickets'
        ORDER BY ordinal_position;
    """)
    for row in rows:
        nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
        default = f" DEFAULT {row['column_default']}" if row['column_default'] else ""
        output.append(f"{row['column_name']:20} {row['udt_name']:15} {nullable:10}{default}")

    output.append("\n=== AI_ANALYSIS TABLE ===")
    rows = await conn.fetch("""
        SELECT column_name, data_type, udt_name, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'ai_analysis'
        ORDER BY ordinal_position;
    """)
    for row in rows:
        nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
        default = f" DEFAULT {row['column_default']}" if row['column_default'] else ""
        output.append(f"{row['column_name']:20} {row['udt_name']:15} {nullable:10}{default}")
        
    await conn.close()
    
    # Write to file
    with open('/app/schema_output.txt', 'w') as f:
        f.write('\n'.join(output))
    
    print('\n'.join(output))

if __name__ == "__main__":
    asyncio.run(inspect_schema())
