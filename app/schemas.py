from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    subscription_status: Optional[str] = "free"
    subscription_expiry: Optional[datetime] = None

    class Config:
        from_attributes = True  # Для Pydantic v2
