from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from decimal import Decimal
from datetime import datetime
from uuid import UUID


# ------------------- AUTH -------------------
class UserBase(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

class TokenData(BaseModel):
    sub: str
    id: UUID
    
class UserCreate(UserBase):
    pass
    password: str

class User(UserBase):
    id: int

# ------------------- BASE SCHEMA -------------------
class CampaignBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Campaign name (3–100 chars)")
    description: Optional[str] = Field(None, max_length=500, description="Short campaign description")
    start_date: datetime
    end_date: datetime
    budget: Decimal = Field(..., gt=0, le=1_000_000, description="Budget must be > 0 and ≤ 1,000,000")
    status: Optional[str] = Field(default="Draft", description="Campaign status")
    created_by: Optional[UUID] = None
    # Validation: End date must be after start date
    @field_validator("end_date")
    def validate_date_range(cls, end_date, info):
        start_date = info.data.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("End date must be after start date.")
        return end_date


# ------------------- CREATE SCHEMA -------------------
class CampaignCreate(CampaignBase):
    pass


# ------------------- UPDATE SCHEMA -------------------
class CampaignUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[Decimal] = Field(None, gt=0, le=1_000_000)
    status: Optional[str] = None
    is_deleted: Optional[bool] = False

    @field_validator("end_date")
    def validate_date_range(cls, end_date, info):
        start_date = info.data.get("start_date")
        if start_date and end_date and end_date <= start_date:
            raise ValueError("End date must be after start date.")
        return end_date


# ------------------- RESPONSE SCHEMA -------------------
class CampaignOutputResponse(CampaignBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_deleted: bool


# class Campaign(CampaignBase):
#     id:int
#     user: Optional[UserBase] = None

    model_config = ConfigDict(from_attributes=True)
