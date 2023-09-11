from fastapi import APIRouter
from app.schemas import user as User_schemas

router = APIRouter()

@router.get("/")
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]

@router.get("/{user_id}", response_model=User_schemas.UserBase)
async def read_user(user_id: int):
    return {"user_id": user_id, "username": "fakeuser"}

