from decimal import Decimal
from typing import List
from schemas.config.rules import CollectionDiscountConfig
from schemas.itemschema import ItemSchema


class DiscountService:
    def __init__(self, config: CollectionDiscountConfig):
        self.config = config
        self.quantization = Decimal("0.01")

    def calculate_discounted_price(self, line_items: List[ItemSchema]) -> dict:
        items = []
        eligible_items = [
            item
            for item in line_items
            if item.collection not in self.config.excluded_collections
        ]
        ineligible_items = [
            item
            for item in line_items
            if item.collection in self.config.excluded_collections
        ]

        rule = self.config.discount_rule

        total_price = Decimal(0)

        if eligible_items:
            # Discount starts from the minimum quantity
            eligible_count = len(eligible_items) - (rule.min_qty - 1)
            discount = eligible_count * rule.discount_percentage
            applied_discount = Decimal((100 - discount) / 100).quantize(
                self.quantization
            )

            for item in eligible_items:
                discounted_price = (item.price * applied_discount).quantize(
                    self.quantization
                )
                items.append(
                    {
                        "name": item.name,
                        "collection": item.collection,
                        "price": float(discounted_price),
                    }
                )
                total_price += discounted_price

        for item in ineligible_items:
            items.append(
                {
                    "name": item.name,
                    "collection": item.collection,
                    "price": float(item.price),
                }
            )
            total_price += item.price

        return {"cart": {"price": float(total_price), "items": items}}
