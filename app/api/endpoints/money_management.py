from typing import List
from fastapi import APIRouter, Depends
from app.models.transaction import TransactionCreate, Transaction, TransactionUpdate
from app.models.monthly_limit import MonthlyLimitCreate, MonthlyLimit
from app.crud import transaction as transaction_crud
from app.crud import monthly_limit as monthly_limit_crud
from app.api.deps import get_current_user
from app.models.user import User
from app.models.api import APIResponse
from app.core.exceptions import NotFoundException

router = APIRouter()

@router.post("/transactions", response_model=APIResponse[Transaction])
async def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user)
):
    new_transaction = await transaction_crud.create_transaction(transaction, current_user.username)
    return APIResponse(status="success", message="Transaction created successfully", data=new_transaction)

@router.get("/transactions", response_model=APIResponse[List[Transaction]])
async def get_user_transactions(current_user: User = Depends(get_current_user)):
    transactions = await transaction_crud.get_user_transactions(current_user.username)
    return APIResponse(status="success", message="Transactions retrieved successfully", data=transactions)

@router.get("/transactions/{transaction_id}", response_model=APIResponse[Transaction])
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user)
):
    transaction = await transaction_crud.get_transaction(transaction_id, current_user.username)
    if not transaction:
        raise NotFoundException("Transaction not found")
    return APIResponse(status="success", message="Transaction retrieved successfully", data=transaction)

@router.put("/transactions/{transaction_id}", response_model=APIResponse[Transaction])
async def update_transaction(
    transaction_id: str,
    transaction_update: TransactionUpdate,
    current_user: User = Depends(get_current_user)
):
    updated_transaction = await transaction_crud.update_transaction(transaction_id, current_user.username, transaction_update)
    if not updated_transaction:
        raise NotFoundException("Transaction not found")
    return APIResponse(status="success", message="Transaction updated successfully", data=updated_transaction)

@router.delete("/transactions/{transaction_id}", response_model=APIResponse[bool])
async def delete_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user)
):
    deleted = await transaction_crud.delete_transaction(transaction_id, current_user.username)
    if not deleted:
        raise NotFoundException("Transaction not found")
    return APIResponse(status="success", message="Transaction deleted successfully", data=True)

@router.post("/monthly-limit", response_model=APIResponse[MonthlyLimit])
async def set_monthly_limit(
    monthly_limit: MonthlyLimitCreate,
    current_user: User = Depends(get_current_user)
):
    new_limit = await monthly_limit_crud.create_or_update_monthly_limit(monthly_limit, current_user.username)
    return APIResponse(status="success", message="Monthly limit set successfully", data=new_limit)

@router.get("/monthly-limit", response_model=APIResponse[MonthlyLimit])
async def get_monthly_limit(current_user: User = Depends(get_current_user)):
    monthly_limit = await monthly_limit_crud.get_monthly_limit(current_user.username)
    if not monthly_limit:
        raise NotFoundException("Monthly limit not set")
    return APIResponse(status="success", message="Monthly limit retrieved successfully", data=monthly_limit)

