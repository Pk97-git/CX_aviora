"""
Consolidated production setup script.
Runs all table creation and population scripts in the correct order.
"""
import asyncio
import os
import sys
import importlib

async def run_setup():
    print("🚀 Aivora Production Setup")
    print("==========================")
    
    # 1. Get Database URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("\n⚠️  DATABASE_URL environment variable not found.")
        print("Please paste your Render Internal Database URL (or External if running locally):")
        db_url = input("DATABASE_URL: ").strip()
        
        if not db_url:
            print("❌ Error: DATABASE_URL is required.")
            return
        
        # Set for subprocesses/imports
        os.environ["DATABASE_URL"] = db_url
    
    print(f"\nUsing Database: {db_url.split('@')[-1] if '@' in db_url else '...'}")
    
    try:
        # 2. Run Analytics Setup
        print("\n[1/4] Creating Analytics Tables...")
        # We use importlib to import modules after setting env var
        import create_analytics_tables
        await create_analytics_tables.create_tables()
        
        print("\n[2/4] Populating Analytics Data...")
        import populate_analytics
        await populate_analytics.populate_analytics()
        
        # 3. Run Executive Setup
        print("\n[3/4] Creating Executive Tables...")
        import create_executive_tables
        await create_executive_tables.create_tables()
        
        print("\n[4/4] Populating Executive Data...")
        import populate_executive_data
        await populate_executive_data.populate_executive_data()
        
        print("\n✅ SETUP COMPLETE!")
        print("All tables created and populated successfully.")
        
    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Add current directory to path so imports work
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        asyncio.run(run_setup())
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
