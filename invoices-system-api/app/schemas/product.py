from pydantic import BaseModel, ConfigDict, validator
from datetime import datetime
from uuid import UUID
from typing import Annotated
from fastapi import Query
from app.core.utils import convert_utc_to_local

class BaseProduct(BaseModel):
    price: Annotated[float, Query(gt=0)]
    title: str
    description: str
    
class CreateProduct(BaseProduct):
    pass

class UpdateProduct(BaseProduct):
    pass

class ResponseProduct(BaseProduct):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime

    @validator("created_at", pre=True)
    def convert_created_at(cls, created_at):
        return convert_utc_to_local(created_at)