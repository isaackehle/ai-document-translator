"""User database model."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from app.core.database import Base


class User(Base):
    """User database model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"))
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=text("now()"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
