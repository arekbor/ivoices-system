from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.models.order_item import OrderItem
import uuid

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, index=True)
    address = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    order_items = relationship(OrderItem, back_populates="order")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", backref="order", uselist=False)