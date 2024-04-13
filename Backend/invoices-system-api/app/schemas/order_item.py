from pydantic import BaseModel
from uuid import UUID

class CreateOrderItem(BaseModel):
    quantity: int
    product_id: UUID