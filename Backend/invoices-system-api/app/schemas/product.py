from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Annotated
from fastapi import Query

class BaseProduct(BaseModel):
    price: Annotated[float, Query(gt=0)]
    title: str
    description: str
    
class CreateProduct(BaseProduct):
    pass

class UpdateProduct(BaseProduct):
    pass

class ResponseProduct(BaseProduct):
    id: UUID
    created_at: datetime