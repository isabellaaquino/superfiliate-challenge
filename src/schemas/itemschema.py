from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


# PRO: Using Pydantic to validate the input data.
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

    # PRO: Price validation to prevent negative prices.
    @field_validator("price")
    @classmethod
    def prevent_zero(cls, value):
        if value < 0:
            raise ValueError(f"Price should be bigger than 0. Given value {value}.")
        return value
