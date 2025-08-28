from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    birth_date: str


class UserCreate(UserBase):
    phone_number: str
    first_name: str
    last_name: str
    birth_date: str
    password: str
    username: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    daily_goal: Optional[int] = None
    monthly_goal: Optional[int] = None
    theme: Optional[str] = None
    language: Optional[str] = None


class User(UserBase):
    id: str
    status: bool = True
    created_at: datetime
    username: str
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    phone_number: Optional[str] = None


class OnboardingSchema(BaseModel):
    week_days_list: list[str]
    monthly_goal: int
    daily_goal: int

