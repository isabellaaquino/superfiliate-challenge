from sqlalchemy import Column, Integer, ForeignKey
from src.database import Base


class CartItem(Base):
    __tablename__ = "cart_item"

    cart_id = Column(Integer, ForeignKey('cart.id'), primary_key=True)
    cart_item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
