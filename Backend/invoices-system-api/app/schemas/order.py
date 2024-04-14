from pydantic import BaseModel, ConfigDict
from annotated_types import Len
from typing import Annotated
from uuid import UUID

from app.schemas.order_item import CreateOrderItem

class BaseOrder(BaseModel):
    name: str
    email: str
    address: str

class CreateOrder(BaseOrder):
    order_items: Annotated[list[CreateOrderItem], Len(min_length=1)]

class ResponseOrder(BaseOrder):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    order_items: list[CreateOrderItem]