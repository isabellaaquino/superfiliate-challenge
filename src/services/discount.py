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
        # ✅ applied_discount = config.apply_discount(eligible_items)
        #
        # It would also improve the flexibility of the service, allowing it to be used in other contexts.
        self.config = config
        self.quantization = Decimal("0.01")

    def calculate_discounted_price(self, line_items: List[ItemSchema]) -> dict:
        items = []
        # ✅ CON: Could create the lists of eligible_items and ineligible_items with a single loop.
        eligible_items = []
        ineligible_items = []
        for item in line_items:
            if item.collection not in self.config.excluded_collections:
                eligible_items.append(item)
            else:
                ineligible_items.append(item)

        applied_discount = self.config.apply_discount(eligible_items)

        # ✅ CON: Could use a map instead of a loop to create the items list.
        items = list(
            map(
                lambda item: self.process_item(
                    item, applied_discount, ineligible_items
                ),
                line_items,
            )
        )

        # ❌ PRO: Re-using the total_price variable to calculate the total price,
        # avoiding an extra iteration at the end.

        # With the usage of map, total price had to be calculated through an extra iteration
        total_price = sum(item["final_price"] for item in items)

        return {
            "cart": {
                "price": float(Decimal(total_price).quantize(self.quantization)),
                "items": items,
            }
        }

    def process_item(self, item, applied_discount, inelegible_items):
        # Removing discount in case the item is ineligible
        if item in inelegible_items:
            applied_discount = 1
        discounted_price = (item.price * applied_discount).quantize(self.quantization)
        return {
            "name": item.name,
            "collection": item.collection,
            # ✅ CON: Could keep the original price and add a new field for the discounted price.
            "price": float(item.price.quantize(self.quantization)),
            "final_price": float(discounted_price),
        }
