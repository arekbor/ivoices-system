from fastapi import APIRouter, Depends
from app.schemas.user import ResponseUser
from app.models.user import User
from app.api.endpoints.user import functions as user_functions
from app.schemas.user import Token

user_router = APIRouter()

@user_router.post("/", response_model=ResponseUser)
async def register_user(
    created_user: User = Depends(user_functions.register_user)
):
    return created_user

@user_router.post("/login", response_model=Token)
async def login_user(
    access_token = Depends(user_functions.login_user)
):
    return access_token

@user_router.get("/", response_model=ResponseUser)
async def read_current_user(
    user: User = Depends(user_functions.get_current_user)
):
    return user