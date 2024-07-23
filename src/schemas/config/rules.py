from typing import List

from pydantic import BaseModel


class DiscountRule(BaseModel):
    min_qty: int
    discount_percentage: float


class ExcludedCollection(BaseModel):
    collection: str


class CollectionDiscountConfig(BaseModel):
    excluded_collections: List[str]
    discount_rule: DiscountRule
