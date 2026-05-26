"""
Database Migration Runner for CareerPilot
Executes the SQL migration file against Supabase
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")


def run_migration():
    """Run the database migration SQL file"""
    migration_file = Path(__file__).parent.parent / "supabase" / "migrations" / "20260524_init.sql"

    if not migration_file.exists():
        print(f"❌ Migration file not found: {migration_file}")
        return False

    print(f"📄 Reading migration file: {migration_file}")
    with open(migration_file, "r", encoding="utf-8") as file_handle:
        sql_content = file_handle.read()

    print(f"🔗 Connecting to Supabase: {SUPABASE_URL}")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

    print("🚀 Executing migration...")
    try:
        print("⚠️  Supabase Python client doesn't support direct SQL execution.")
        print("📝 Using psycopg2 to connect directly to the database...")
        print("\n⚠️  To run the migration, you need the database password.")
        print(
            "Get it from: https://supabase.com/dashboard/project/atwlzuxjblqlonrdbwtt/settings/database"
        )
        print("\nOr run this SQL manually in the Supabase SQL Editor:")
        print("=" * 80)
        print(sql_content)
        print("=" * 80)
        return False
    except Exception as exc:
        print(f"❌ Migration failed: {exc}")
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("CareerPilot Database Migration")
    print("=" * 80)
    run_migration()
