"""Create users table manually."""
import asyncio
import asyncpg


async def create_table():
    """Create users table."""
    conn = await asyncpg.connect('postgresql://postgres:postgres@127.0.0.1:54322/postgres')

    # Create users table
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            is_superuser BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    ''')

    # Create indexes
    await conn.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)')
    await conn.execute('CREATE INDEX IF NOT EXISTS idx_users_id ON users (id)')

    # Verify table
    tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    print(f'Tables: {[t["tablename"] for t in tables]}')

    await conn.close()
    print('✅ Users table created successfully!')


if __name__ == '__main__':
    asyncio.run(create_table())
