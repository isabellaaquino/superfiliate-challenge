from typing import List

from pydantic import BaseModel


class DiscountRule(BaseModel):
    id: int
    min_qty: int
    discount_percentage: float


class ExcludedCollection(BaseModel):
    id: int
    collection: str


class CollectionDiscountConfig(BaseModel):
    excluded_collections: List[str]
    discount_rule: DiscountRule
