"""
Database Setup Script for CareerPilot
Prints the SQL migration instructions for manual execution.
"""

import asyncio
from pathlib import Path


async def setup_database():
    """Load the migration SQL and print setup instructions."""
    print("=" * 80)
    print("CareerPilot Database Setup")
    print("=" * 80)

    migration_file = Path(__file__).parent.parent / "supabase" / "migrations" / "20260524_init.sql"
    with open(migration_file, "r", encoding="utf-8") as file_handle:
        sql_content = file_handle.read()

    print("\n📋 Migration SQL loaded successfully")
    print(f"📏 SQL length: {len(sql_content)} characters")

    print("\n" + "=" * 80)
    print("⚠️  MANUAL STEP REQUIRED")
    print("=" * 80)
    print("\nThe Supabase Python client doesn't support direct SQL execution.")
    print("Please run the migration manually using ONE of these methods:")
    print("\n📍 METHOD 1: Supabase Dashboard (Easiest)")
    print("   1. Go to: https://supabase.com/dashboard/project/atwlzuxjblqlonrdbwtt/editor")
    print("   2. Click 'New Query'")
    print("   3. Copy the SQL from: supabase/migrations/20260524_init.sql")
    print("   4. Paste and click 'Run'")
    print("\n📍 METHOD 2: Supabase CLI")
    print("   1. Install: npm install -g supabase")
    print("   2. Login: supabase login")
    print("   3. Link: supabase link --project-ref atwlzuxjblqlonrdbwtt")
    print("   4. Push: supabase db push")
    print("\n📍 METHOD 3: I can open the SQL file for you to copy")

    response = input("\nWould you like me to display the SQL here? (y/n): ")
    if response.lower() == "y":
        print("\n" + "=" * 80)
        print("COPY THIS SQL TO SUPABASE SQL EDITOR:")
        print("=" * 80)
        print(sql_content)
        print("=" * 80)

    print("\n✅ After running the SQL, your database will be ready!")


if __name__ == "__main__":
    asyncio.run(setup_database())
