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
from src.crud.item import get_items
from src.crud.item import create_item as create_item_crud

router = APIRouter(prefix="/cart")


@router.get("/checkout", status_code=status.HTTP_200_OK)
async def create_item(cart: CartSchema, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Calculates the final price of a given cart

    Args:
        item_data (Item): Item request
        db (Session): Database session.

    Returns:
        Item: Item created.
    """
    new_item = ItemDB(**item_data.dict())

    if (db.query(ItemDB).filter(ItemDB.name == new_item.name)
            .filter(ItemDB.collection == item_data.collection).first()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is already an existing item with that name and collection. Please try again.")

    create_item_crud(db, new_item)
    return new_item


