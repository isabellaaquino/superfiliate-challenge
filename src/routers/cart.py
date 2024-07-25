from fastapi import Depends
from starlette import status
from fastapi import APIRouter
from starlette.responses import JSONResponse
from typing import List

from schemas.config.rules import CollectionDiscountConfig
from services.discount import DiscountService
from schemas.cartschema import CartAPISchema
from config import get_config

router = APIRouter(prefix="/cart")


@router.post("/checkout", status_code=status.HTTP_200_OK)
async def checkout_cart(
    cart_api: CartAPISchema,
    # Question: Curious to understand the use case of receiving the config as a dependency here.
    config: CollectionDiscountConfig = Depends(get_config),
) -> JSONResponse:
    """
    Calculates the final price of a given cart

    Args:
        cart (CartSchema): CartSchema request
        config (CollectionDiscountConfig): Current server configuration of discounts

    Returns:
        JSONResponse: JSON containing the final price and unit prices.
    """

    # PRO: Using the DiscountService to calculate the final price, leaving a clean route function.
    price_dict = DiscountService(config=config).calculate_discounted_price(
        cart_api.cart.lineItems
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content=price_dict)
