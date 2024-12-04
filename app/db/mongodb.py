from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def get_database():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    return client.get_database("money_tracer")

