from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field
from src.schemas.cart_item import CartItem

class Cart(BaseModel):
    """
    Base model mirroring the database model
    Represents an item that can be added to a certain Cart
    """

    reference: str = Field(min_length=8, max_length=8)
    lineItems: list[CartItem] = Field(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True
