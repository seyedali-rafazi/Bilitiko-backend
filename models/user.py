"""User model using Beanie ODM."""

from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import EmailStr, Field
import bcrypt


class User(Document):
    """User document model."""

    email: EmailStr = Field(unique=True, index=True)
    phone: Optional[str] = None
    first_name: str
    last_name: str
    hashed_password: str

    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False

    date_joined: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"
        indexes = [
            "email",
        ]

    def verify_password(self, plain_password: str) -> bool:
        """Verify a password against the hash."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self.hashed_password.encode("utf-8"),
        )

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate password hash."""
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    def get_full_name(self) -> str:
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self) -> str:
        """Return the user's first name."""
        return self.first_name

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "phone": "+1234567890",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            }
        }


# Made with Bob
