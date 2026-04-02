"""Test database connection."""

import asyncio
import asyncpg
from app.core.config import settings


async def test_connection():
    """Test database connection."""
    # Convert asyncpg URL to standard postgres URL for asyncpg.connect
    db_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    print(f"Testing connection to: {db_url}")
    print("-" * 60)

    try:
        # Parse connection URL
        conn = await asyncpg.connect(db_url)
        print("✅ Connection successful!")

        # Get PostgreSQL version
        version = await conn.fetchval("SELECT version();")
        print(f"\nPostgreSQL Version: {version}")

        # Get current database
        database = await conn.fetchval("SELECT current_database();")
        print(f"Database: {database}")

        # Get current user
        user = await conn.fetchval("SELECT current_user;")
        print(f"User: {user}")

        # Check for tables
        tables = await conn.fetch(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        )
        if tables:
            print(f"\n📊 Tables found: {[t['tablename'] for t in tables]}")
        else:
            print("\n⚠️  No tables found in public schema")
        print("\n✅ Connection test passed!")
        return True

    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(test_connection())
