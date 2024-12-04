from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    title: str
    description: Optional[str] = None
    nominal: float
    category_name: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    nominal: Optional[float] = None
    category_name: Optional[str] = None

