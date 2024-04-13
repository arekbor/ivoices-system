from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.schemas.product import CreateProduct, UpdateProduct
from app.models.user import User
from app.api.endpoints.user import functions as user_functions
from app.models.product import Product
from app.core.dependencies import get_db
from uuid import UUID

def create_product(
    product: CreateProduct, 
    db: Session = Depends(get_db), 
    user: User = Depends(user_functions.get_current_user)
) -> Product:
    new_product = Product(
        price=product.price,
        title=product.title,
        description=product.description,
        user_id=user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def read_all_products(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
) -> list[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(
    product_id: UUID, 
    data: UpdateProduct, 
    db: Session = Depends(get_db), 
    user: User = Depends(user_functions.get_current_user)
) -> Product:
    db_product = db.query(Product).filter(and_(Product.id == product_id, Product.user_id == user.id)).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found"
        )
    db_product.description = data.description
    db_product.price = data.price
    db_product.title = data.title
    db.commit()
    db.refresh(db_product)
    return db_product