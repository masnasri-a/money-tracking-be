from app.models.monthly_limit import MonthlyLimitCreate, MonthlyLimit, MonthlyLimitUpdate
from app.db.mongodb import get_database
from bson import ObjectId

async def create_or_update_monthly_limit(monthly_limit: MonthlyLimitCreate, user_id: str) -> MonthlyLimit:
    db = await get_database()
    monthly_limits_collection = db["monthly_limits"]
    
    monthly_limit_dict = monthly_limit.dict()
    monthly_limit_dict["user_id"] = user_id
    
    result = await monthly_limits_collection.update_one(
        {"user_id": user_id},
        {"$set": monthly_limit_dict},
        upsert=True
    )
    
    if result.upserted_id:
        monthly_limit_dict["id"] = str(result.upserted_id)
    else:
        existing_limit = await monthly_limits_collection.find_one({"user_id": user_id})
        monthly_limit_dict["id"] = str(existing_limit["_id"])
    
    return MonthlyLimit(**monthly_limit_dict)

async def get_monthly_limit(user_id: str) -> MonthlyLimit:
    db = await get_database()
    monthly_limits_collection = db["monthly_limits"]
    
    monthly_limit = await monthly_limits_collection.find_one({"user_id": user_id})
    
    if monthly_limit:
        return MonthlyLimit(**monthly_limit, id=str(monthly_limit["_id"]))
    return None

