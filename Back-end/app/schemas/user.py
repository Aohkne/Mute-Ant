from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Profile(BaseModel):
    name: str
    gender: str
    avatar: str
    dateOfBirth: datetime
    address: str
    phoneNum: str

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    profile: Profile
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
