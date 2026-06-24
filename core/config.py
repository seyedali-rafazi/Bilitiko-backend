"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings
from typing import List
from decouple import config
from urllib.parse import quote_plus


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "Aircraft Tickets API"
    VERSION: str = "1.0.0"
    DEBUG: bool = config("DEBUG", default=True, cast=bool)

    # Security
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "JWT_ACCESS_TOKEN_LIFETIME", default=60, cast=int
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = config(
        "JWT_REFRESH_TOKEN_LIFETIME", default=1440, cast=int
    )

    # MongoDB
    MONGODB_URI: str = config("MONGODB_URI")
    MONGODB_NAME: str = config("MONGODB_NAME", default="aircraft_tickets")

    # CORS
    CORS_ORIGINS: List[str] = config(
        "CORS_ALLOWED_ORIGINS", default="http://localhost:3000,http://127.0.0.1:3000"
    ).split(",")

    @property
    def mongodb_url(self) -> str:
        """Get MongoDB connection URL."""
        # The URI should already have the encoded password
        # Just append the database name if needed
        uri = self.MONGODB_URI
        if not uri.endswith("/"):
            uri += "/"
        return uri

    class Config:
        case_sensitive = True


settings = Settings()

# Made with Bob
