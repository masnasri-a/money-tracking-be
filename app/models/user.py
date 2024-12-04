from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(UserCreate):
    hashed_password: str
    profile_picture: str = None

class User(BaseModel):
    username: str
    email: EmailStr
    profile_picture: str = None

class UserUpdate(BaseModel):
    email: EmailStr = None
    profile_picture: str = None

class Token(BaseModel):
    access_token: str
    token_type: str

