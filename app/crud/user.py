from app.models.user import UserCreate, UserInDB, UserUpdate
from app.core.security import get_password_hash
from app.db.mongodb import get_database
from bson import ObjectId

async def create_user(user: UserCreate) -> UserInDB:
    db = await get_database()
    users_collection = db["users"]
    
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
    
    result = await users_collection.insert_one(user_in_db.dict())
    return user_in_db

async def get_user(username: str):
    db = await get_database()
    users_collection = db["users"]
    
    user = await users_collection.find_one({"username": username})
    if user:
        if not user["profile_picture"]:
            user["profile_picture"] = "None"
        return UserInDB(**user)
    return None

async def update_user(username: str, user_update: UserUpdate):
    db = await get_database()
    users_collection = db["users"]
    
    update_data = user_update.dict(exclude_unset=True)
    await users_collection.update_one({"username": username}, {"$set": update_data})
    
    updated_user = await users_collection.find_one({"username": username})
    return UserInDB(**updated_user)

