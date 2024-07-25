from decimal import Decimal
from typing import List
from schemas.config.rules import CollectionDiscountConfig
from schemas.itemschema import ItemSchema


class DiscountService:
    def __init__(self, config: CollectionDiscountConfig):
        # PRO: Discount service can work with multiple discount configurations.
        # One possible improvement here would be to allow the service deal with any type of discount,
        # and not only CollectionDiscountConfig. (minimum quantity + discount percentage). Something
        # we could easily ply like this:
        #
        # applied_discount = config.apply_discount(eligible_items)
        #
        # It would also improve the flexibility of the service, allowing it to be used in other contexts.
        self.config = config
        self.quantization = Decimal("0.01")

    def calculate_discounted_price(self, line_items: List[ItemSchema]) -> dict:
        items = []
        # CON: Could create the lists of eligible_items and ineligible_items with a single loop.
        #
        # eligible_items = []
        # ineligible_items = []
        # for item in line_items:
        #     if item.collection not in self.config.excluded_collections:
        #         eligible_items.append(item)
        #     else:
        #         ineligible_items.append(item)
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

        # PRO: Re-using the total_price variable to calculate the total price,
        # avoiding an extra iteration at the end.
        total_price = Decimal(0)

        if eligible_items:
            # Discount starts from the minimum quantity
            eligible_count = len(eligible_items) - (rule.min_qty - 1)
            discount = eligible_count * rule.discount_percentage
            applied_discount = Decimal((100 - discount) / 100).quantize(
                self.quantization
            )

            # CON: Could use a map instead of a loop to create the items list.
            for item in eligible_items:
                discounted_price = (item.price * applied_discount).quantize(
                    self.quantization
                )
                items.append(
                    {
                        "name": item.name,
                        "collection": item.collection,
                        # CON: Could keep the original price and add a new field for the discounted price.
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
