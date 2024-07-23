from decimal import Decimal
from typing import List
from src.schemas.config.rules import CollectionDiscountConfig
from src.schemas.itemschema import ItemSchema


class DiscountService:
    def __init__(self, config: CollectionDiscountConfig):
        self.config = config

    def calculate_discounted_price(self, line_items: List[ItemSchema]) -> float:
        eligible_items = [item for item in line_items if item.collection not in self.config.excluded_collections]
        ineligible_items = [item for item in line_items if item.collection in self.config.excluded_collections]

        rule = self.config.discount_rule

        total_price = float(0)

        if eligible_items:
            eligible_count = len(eligible_items)
            if eligible_count >= rule.min_qty:
                discount = Decimal((100 - rule.discount_percentage) / 100)
                discounted_price = sum(item["price"] for item in eligible_items) * discount
                total_price += discounted_price

        total_price += sum(item["price"] for item in ineligible_items)
        return total_price
