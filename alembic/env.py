"""Database migrations configuration."""

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context  # type: ignore

# Import your models
from app.core.database import Base
from app.core.config import settings

# this is the Alembic Config object
alembic_config = context.config

# Interpret the config file for Python logging
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Model's MetaData object for 'autogenerate' support
target_metadata = Base.metadata


def get_url():
    """Get database URL from settings."""
    return settings.DATABASE_URL


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Use synchronous driver for migrations
    configuration = alembic_config.get_section(alembic_config.config_ini_section)
    # Replace asyncpg with psycopg2 for migrations
    url = get_url().replace("postgresql+asyncpg://", "postgresql://")
    configuration["sqlalchemy.url"] = url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
