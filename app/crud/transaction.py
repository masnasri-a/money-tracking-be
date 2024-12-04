from app.models.transaction import TransactionCreate, Transaction, TransactionUpdate
from typing import List
from app.db.mongodb import get_database
from bson import ObjectId
from datetime import datetime

async def create_transaction(transaction: TransactionCreate, user_id: str) -> Transaction:
    db = await get_database()
    transactions_collection = db["transactions"]
    
    transaction_dict = transaction.dict()
    transaction_dict["user_id"] = user_id
    transaction_dict["created_at"] = datetime.utcnow()
    
    result = await transactions_collection.insert_one(transaction_dict)
    
    return Transaction(**transaction_dict, id=str(result.inserted_id))
async def get_user_transactions(user_id: str) -> List[Transaction]:
    db = await get_database()
    transactions_collection = db["transactions"]
    
    cursor = transactions_collection.find({"user_id": user_id})
    transactions = await cursor.to_list(length=None)
    
    return [Transaction(**transaction, id=str(transaction["_id"])) for transaction in transactions]

async def get_transaction(transaction_id: str, user_id: str) -> Transaction:
    db = await get_database()
    transactions_collection = db["transactions"]
    
    transaction = await transactions_collection.find_one({"_id": ObjectId(transaction_id), "user_id": user_id})
    
    if transaction:
        return Transaction(**transaction, id=str(transaction["_id"]))
    return None

async def update_transaction(transaction_id: str, user_id: str, transaction_update: TransactionUpdate) -> Transaction:
    db = await get_database()
    transactions_collection = db["transactions"]
    
    update_data = transaction_update.dict(exclude_unset=True)
    await transactions_collection.update_one(
        {"_id": ObjectId(transaction_id), "user_id": user_id},
        {"$set": update_data}
    )
    
    updated_transaction = await transactions_collection.find_one({"_id": ObjectId(transaction_id), "user_id": user_id})
    return Transaction(**updated_transaction, id=str(updated_transaction["_id"]))

async def delete_transaction(transaction_id: str, user_id: str) -> bool:
    db = await get_database()
    transactions_collection = db["transactions"]
    
    result = await transactions_collection.delete_one({"_id": ObjectId(transaction_id), "user_id": user_id})
    return result.deleted_count > 0

