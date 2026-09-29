from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.profile import ProfileResponse

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=6, max_length=128, example="SecretPass123!")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="SecretPass123!")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    profile: Optional[ProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
