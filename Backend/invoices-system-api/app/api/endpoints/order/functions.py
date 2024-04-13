from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.order import CreateOrder
from app.models.user import User
from app.models.product import Product
from app.models.order_item import OrderItem
from app.models.order import Order
from app.api.endpoints.user import functions as user_functions

def create_order(
    data: CreateOrder, 
    db: Session = Depends(get_db), 
    user: User = Depends(user_functions.get_current_user)
) -> Order:
    product_ids = [item.product_id for item in data.order_items]
    db_products = db.query(Product).filter(and_(Product.id.in_(product_ids), Product.user_id == user.id)).all()
    if len(db_products) is not len(product_ids):
        missing_product_ids = set(product_ids) - set([p.id for p in db_products])
        detail_message = "Products IDs: {} do not exist.".format(', '.join(str(pid) for pid in missing_product_ids))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail_message
        )
    order_items = [
        OrderItem(quantity=item.quantity, product_id=item.product_id)
        for item in data.order_items
    ]
    order = Order(
        name=data.name, 
        email=data.email,
        address=data.address,
        order_items=order_items,
        user_id=user.id
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order