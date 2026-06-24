"""Database configuration and initialization."""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings


class Database:
    """Database connection manager."""

    client: AsyncIOMotorClient = None

    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB and initialize Beanie."""
        # Use directConnection=False to allow SRV resolution with fallback
        cls.client = AsyncIOMotorClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=30000,  # Increased timeout
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            directConnection=False,
            retryWrites=True,
            w="majority",
        )

        # Import all models here
        from models.user import User
        from models.flight import Flight, City, PopularFlight, Destination
        from models.booking import Booking
        from models.transport import TransportTrip, TransportRoute
        from models.insurance import Insurance

        # Initialize Beanie with all document models
        await init_beanie(
            database=cls.client[settings.MONGODB_NAME],
            document_models=[
                User,
                Flight,
                City,
                PopularFlight,
                Destination,
                Booking,
                TransportTrip,
                TransportRoute,
                Insurance,
            ],
        )
        print(f"Connected to MongoDB: {settings.MONGODB_NAME}")

    @classmethod
    async def close_db(cls):
        """Close database connection."""
        if cls.client:
            cls.client.close()
            print("Closed MongoDB connection")


# Database instance
db = Database()

# Made with Bob
