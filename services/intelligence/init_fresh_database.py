"""
Fresh database initialization script
Drops all tables and creates fresh schema with sample data
"""
import asyncio
import asyncpg
import os

async def init_database():
    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )
    
    if not DATABASE_URL:
        print("❌ ERROR: DATABASE_URL environment variable not set")
        print("Please set DATABASE_URL before running this script")
        return
    
    
    # Convert asyncpg URL format
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    print("Connecting to database...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        # Read initialization SQL
        print("Reading initialization script...")
        with open('init_fresh_database.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Execute initialization
        print("Executing database initialization...")
        print("⚠️  WARNING: This will DROP all existing tables!")
        
        await conn.execute(sql)
        
        print("\n✓ Database initialized successfully!")
        print("\n" + "="*60)
        print("📊 REALISTIC COMPANY DATA CREATED")
        print("="*60)
        print("\n🏢 Companies:")
        print("  1. TechStart Inc (SaaS Startup) - Pro Plan")
        print("     - 4 users, 5 tickets, 3 integrations")
        print("  2. RetailPro Solutions (E-commerce) - Enterprise Plan")
        print("     - 4 users, 4 tickets, 2 integrations")
        print("  3. CloudBase (Cloud Infrastructure) - Enterprise Plan")
        print("     - 3 users, 2 tickets, 2 integrations")
        
        print("\n👥 Total Users: 11")
        print("  - 3 Admins, 3 Managers, 5 Agents")
        
        print("\n🎫 Total Tickets: 12")
        print("  - Varied scenarios: refunds, bugs, features, shipping issues")
        print("  - Complete AI analysis on all tickets")
        print("  - Realistic customer interactions")
        
        print("\n💬 Total Comments: 8")
        print("  - Mix of customer replies and internal notes")
        
        print("\n🔗 Total Integrations: 7")
        print("  - Freshdesk, Zendesk, Slack, JIRA")
        
        print("\n🔐 LOGIN CREDENTIALS (All Companies):")
        print("  Password for ALL users: password123")
        print("\n  TechStart Inc:")
        print("    admin:   sarah.chen@techstart.io")
        print("    manager: mike.rodriguez@techstart.io")
        print("    agent:   emily.watson@techstart.io")
        print("\n  RetailPro Solutions:")
        print("    admin:   admin@retailpro.com")
        print("    manager: carlos.martinez@retailpro.com")
        print("\n  CloudBase:")
        print("    admin:   admin@cloudbase.io")
        print("    manager: priya.patel@cloudbase.io")
        
        print("\n" + "="*60)
        print("✅ Database is ready for production-like testing!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error initializing database: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_database())
