"""User repository for database operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User-specific repository with custom queries."""

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        """
        Get user by email.

        Args:
            db: Database session
            email: User email

        Returns:
            Optional[User]: User if found
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def is_active(self, db: AsyncSession, user_id: int) -> bool:
        """
        Check if user is active.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            bool: True if user is active
        """
        user = await self.get(db, user_id)
        return bool(user.is_active) if user else False  # pyright: ignore[reportOptionalOperand]


# Singleton instance
user_repository = UserRepository(User)
