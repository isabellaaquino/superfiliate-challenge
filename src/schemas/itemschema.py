from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class ItemSchema(BaseModel):
    """
    Base model mirroring the database model
    Represents an item that can be added to carts
    """

    name: str
    price: Decimal = Field(max_digits=10, decimal_places=2, ge=0)
    collection: str

    class Config:
        from_attributes = True

    @field_validator('price')
    def prevent_zero(self, value):
        if value < 0: 
            raise ValueError(f'Price should be bigger than 0. Given value {value}.')
        return value
