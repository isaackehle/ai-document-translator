"""Run migrations manually."""

import sys

sys.path.insert(0, ".")

from alembic import command  # pyright: ignore[reportAttributeAccessIssue]
from alembic.config import Config

# Load Alembic config
alembic_cfg = Config("alembic.ini")

# Run upgrade
print("Running migrations...")
command.upgrade(alembic_cfg, "head")
print("Migrations completed!")
