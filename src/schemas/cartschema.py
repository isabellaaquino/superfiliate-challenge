from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, field_validator
from schemas.itemschema import ItemSchema


class CartSchema(BaseModel):
    """
    Base model mirroring the database model
    Represents an item that can be added to a certain Cart
    """

    reference: str = Field(min_length=36, max_length=36)
    lineItems: List[ItemSchema]

    class Config:
        from_attributes = True

    @field_validator("reference")
    @classmethod
    def validate_reference(cls, reference):
        # Creating constraint for reference keys
        if len(reference) != 36:
            raise ValueError(
                f"Reference should be 36 characters. Given value {reference}."
            )
        return reference


class CartAPISchema(BaseModel):
    cart: CartSchema
