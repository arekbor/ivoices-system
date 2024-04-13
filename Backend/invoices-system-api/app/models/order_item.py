from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    quantity = Column(Integer, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    product = relationship("Product", backref="order_items", uselist=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    order = relationship("Order", back_populates="order_items", uselist=False)