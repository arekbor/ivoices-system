from fastapi import APIRouter, Depends
from app.models.order import Order
from app.schemas.order import ResponseOrder
from app.api.endpoints.order import functions as order_functions

order_router = APIRouter()

@order_router.post("/", response_model=ResponseOrder)
async def create_order(
    order: Order = Depends(order_functions.create_order)
):
    return order
