from fastapi import APIRouter, Depends
from app.schemas.product import ResponseProduct
from app.models.user import User
from app.models.product import Product
from app.api.endpoints.product import functions as product_functions
from app.api.endpoints.user import functions as user_functions

product_router = APIRouter()

@product_router.post("/", response_model=ResponseProduct)
async def create_product(
    product: Product = Depends(product_functions.create_product)
):
    return product

@product_router.get("/", response_model=list[ResponseProduct])
async def read_all_products(
    products: list[Product] = Depends(product_functions.read_all_products),
    _:User = Depends(user_functions.get_current_user)
):
    return products

@product_router.put("/{product_id}", response_model=ResponseProduct)
async def update_product(
    updated_product: Product = Depends(product_functions.update_product)
):
    return updated_product