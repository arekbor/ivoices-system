from fastapi import APIRouter
from app.api.endpoints.order.router import order_router
from app.api.endpoints.product.router import product_router
from app.api.endpoints.user.router import user_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(product_router, prefix="/products", tags=["products"])
api_router.include_router(order_router, prefix="/orders", tags=["orders"])