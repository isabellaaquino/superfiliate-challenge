import datetigetme

from fastapi import HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter
from starlette.responses import JSONResponse
from typing import List

from src.database import get_db
from src.database_models.item import Item as ItemDB
from src.schemas.cartschema import CartSchema
from src.crud.item import get_item as get_item_crud

router = APIRouter(prefix="/cart")


@router.get("/checkout", status_code=status.HTTP_200_OK)
async def checkout_cart(cart: CartSchema, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Calculates the final price of a given cart

    Args:
        cart (CartSchema): CartSchema request
        db (Session): Database session.

    Returns:
        Item: Item created.
    """
    for item in cart.lineItems:
        item_db = ItemDB(item)
        if not get_item_crud(db, item_db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There is no such item with that name and collection. Please try again.")

    return JSONResponse(status_code=status.HTTP_200_OK, content=cart)
