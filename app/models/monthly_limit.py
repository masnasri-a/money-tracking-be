from pydantic import BaseModel
from typing import Optional

class MonthlyLimitBase(BaseModel):
    nominal: float

class MonthlyLimitCreate(MonthlyLimitBase):
    pass

class MonthlyLimit(MonthlyLimitBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True

class MonthlyLimitUpdate(BaseModel):
    nominal: Optional[float] = None

