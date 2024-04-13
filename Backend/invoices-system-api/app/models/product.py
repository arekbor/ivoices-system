from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    price = Column(Float, index=True)
    title = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", backref="product", uselist=False)