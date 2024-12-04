from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import UserCreate, User, Token, UserUpdate
from app.crud.user import create_user, get_user, update_user
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.config import settings
from app.api.deps import get_current_user
from app.core.file_handler import save_upload_file
from app.models.api import APIResponse
from app.core.exceptions import BadRequestException, UnauthorizedException

router = APIRouter()

@router.post("/register", response_model=APIResponse[User])
async def register(user: UserCreate):
    db_user = await get_user(user.username)
    if db_user:
        raise BadRequestException("Username already registered")
    new_user = await create_user(user)
    return APIResponse(status="success", message="User registered successfully", data=new_user)

@router.post("/token", response_model=APIResponse[Token])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedException("Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return APIResponse(status="success", message="Login successful", data={"access_token": access_token, "token_type": "bearer"})

@router.get("/users/me", response_model=APIResponse[User])
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return APIResponse(status="success", message="User profile retrieved successfully", data=current_user)

@router.put("/users/me", response_model=APIResponse[User])
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    if user_update.profile_picture:
        profile_picture_url = await save_upload_file(user_update.profile_picture, current_user.username)
        user_update.profile_picture = profile_picture_url
    
    updated_user = await update_user(current_user.username, user_update)
    return APIResponse(status="success", message="User profile updated successfully", data=updated_user)

