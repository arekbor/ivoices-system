from pydantic import BaseModel, ConfigDict, computed_field, validator
from annotated_types import Len
from typing import Annotated
from uuid import UUID
from datetime import datetime
from app.core.utils import convert_utc_to_local
from app.schemas.order_item import CreateOrderItem, ResponseOrderItem

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
    order_items: list[ResponseOrderItem]
    created_at: datetime

    @validator("created_at", pre=True)
    def convert_created_at(cls, created_at):
        return convert_utc_to_local(created_at)
        
    @computed_field()
    def total_due(self) -> float:
        return sum((item.product.price*item.quantity) for item in self.order_items)
