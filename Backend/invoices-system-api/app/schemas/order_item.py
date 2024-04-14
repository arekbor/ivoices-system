from pydantic import BaseModel, ConfigDict
from uuid import UUID

class CreateOrderItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    quantity: int
    product_id: UUID