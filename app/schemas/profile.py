from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime

class ProfileBase(BaseModel):
    phone_number: Optional[str] = Field(None, example="+1234567890", max_length=20)
    address: Optional[str] = Field(None, example="123 Main St, Springfield")
    date_of_birth: Optional[date] = Field(None, example="1995-06-15")
    bio: Optional[str] = Field(None, example="Software engineer and tech enthusiast.")

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    phone_number: Optional[str] = Field(None, example="+1234567890", max_length=20)
    address: Optional[str] = Field(None, example="456 Elm St, Metropolis")
    date_of_birth: Optional[date] = Field(None, example="1995-06-15")
    bio: Optional[str] = Field(None, example="Updated bio: full-stack developer.")

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
