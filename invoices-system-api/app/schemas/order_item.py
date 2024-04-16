from pydantic import BaseModel, ConfigDict, computed_field
from uuid import UUID
from app.schemas.product import ResponseProduct

class BaseOrderItem(BaseModel):
    quantity: int
    product_id: UUID

class CreateOrderItem(BaseOrderItem):
    pass

class ResponseOrderItem(BaseOrderItem):
    model_config = ConfigDict(from_attributes=True)
    product: ResponseProduct

    @computed_field()
    def total_price(self) -> float:
        return self.quantity*self.product.price