## models_user.py
"""
see https://odmantic.readthedocs.io/en/stable/tutorial/quick-start/
this code is user model definition for odmantic
"""

from odmantic import Field, Model, EmailStr
import datetime

class User(Model):
    user_name: str = Field(..., max_length=30, unique=True)
    name: str | None = Field(None, max_length=30)
    #email: EmailStr = Field(..., unique=True)
    is_private: bool = False
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)