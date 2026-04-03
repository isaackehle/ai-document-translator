"""User service for business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.repositories.user_repository import user_repository
from app.schemas.user import User, UserCreate, UserUpdate


class UserService:
    """
    Business logic for user operations.

    Handles user creation, authentication, and updates.
    """

    def __init__(self):
        self.repository = user_repository

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """
        Create new user with hashed password.

        Args:
            db: Database session
            user_in: User creation data

        Returns:
            User: Created user

        Raises:
            ValueError: If email already exists
        """
        # Check if email exists
        existing = await self.repository.get_by_email(db, user_in.email)
        if existing:
            raise ValueError("Email already registered")

        # Hash password
        user_in_dict = user_in.model_dump()
        user_in_dict["hashed_password"] = get_password_hash(user_in_dict.pop("password"))

        # Create user
        user = await self.repository.create(db, UserCreate(**user_in_dict))  # pyright: ignore[reportCallIssue]
        return user

    async def authenticate(self, db: AsyncSession, email: str, password: str) -> User | None:
        """
        Authenticate user with email and password.

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            Optional[User]: User if authenticated
        """
        user = await self.repository.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, str(user.hashed_password)):  # pyright: ignore[reportArgumentType]
            return None
        return user

    async def update_user(self, db: AsyncSession, user_id: int, user_in: UserUpdate) -> User | None:
        """
        Update user.

        Args:
            db: Database session
            user_id: User ID
            user_in: Update data

        Returns:
            Optional[User]: Updated user
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None

        # Hash password if provided
        if user_in.password:
            update_data = user_in.model_dump(exclude_unset=True)
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
            user_in = UserUpdate(**update_data)

        return await self.repository.update(db, user, user_in)


# Singleton instance
user_service = UserService()
