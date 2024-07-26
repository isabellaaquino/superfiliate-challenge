from decimal import Decimal
from typing import List

from pydantic import BaseModel


class DiscountRule(BaseModel):
    min_qty: int
    discount_percentage: float
    max_discount: float


class ExcludedCollection(BaseModel):
    collection: str


class DiscountConfigBase(BaseModel):
    def apply_discount(self, eligible_items):
        raise NotImplementedError


class CollectionDiscountConfig(DiscountConfigBase):
    excluded_collections: List[str]
    discount_rule: DiscountRule

    def apply_discount(self, eligible_items):
        applied_discount = Decimal("1.00")
        if eligible_items:
            # Discount starts from the minimum quantity
            eligible_count = len(eligible_items) - (self.discount_rule.min_qty - 1)
            discount = eligible_count * self.discount_rule.discount_percentage
            if discount > self.discount_rule.max_discount:
                discount = self.discount_rule.max_discount
            applied_discount = Decimal((100 - discount) / 100).quantize(Decimal("0.01"))
        return applied_discount
