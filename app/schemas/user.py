## schemas_user.py

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    id: int = Field(..., gt=0)
    username: str = Field(..., max_length=30)
    #email: EmailStr
    full_name: str | None = Field(None, max_length=30)
    is_private: bool = False
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    username: str
    email: EmailStr
    full_name: str | None = Field(None, max_length=30)
    is_private: bool = False