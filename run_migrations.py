"""Run migrations manually."""
import sys
sys.path.insert(0, '.')

from alembic.config import Config
from alembic import command

# Load Alembic config
alembic_cfg = Config("alembic.ini")

# Run upgrade
print("Running migrations...")
command.upgrade(alembic_cfg, "head")
print("Migrations completed!")
