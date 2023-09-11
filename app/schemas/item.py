## schemas_item.py

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ItemBase(BaseModel):
    name: str  
    price: float = Field(..., gt=0)
    description: str | None = Field(None, max_length=300)
    tax: float | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True

class Item(ItemBase):
    pass

class ItemCreate(ItemBase):
    name: str
    description: str | None = Field(None, max_length=300)
    price: float = Field(..., gt=0)
    tax: float | None = None
    updated_at: datetime = Field(default_factory=datetime.now)

