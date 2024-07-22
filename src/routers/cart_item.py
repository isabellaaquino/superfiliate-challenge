import datetigetme

from fastapi import HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette import status
from fastapi import APIRouter
from starlette.responses import JSONResponse
from typing import List

from src.database import get_db
from src.database_models.item import Item as ItemDB
from src.schemas.itemschema import ItemSchema as ItemModel
from src.crud.item import get_items
from src.crud.item import create_item as create_item_crud

router = APIRouter(prefix="/item")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ItemModel)
async def create_item(item_data: ItemModel, db: Session = Depends(get_db)) -> ItemModel:
    """
    Create a new cart item from a coming request

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


@router.get("", response_model=List[ItemModel])
async def list_sensor_data(
        *, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ItemModel]:
    """
    List all cart item.

    Args:
        offset (int): Offset to start the list.
        limit (int):  Limit of cart items to be listed.
        db (Session): Database session.

    Returns:
        list[item]: List of all cart items.
    """
    is_date_range_invalid = offset < 0 or limit < 0 or limit > 100

    if is_date_range_invalid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offset and limit have to be valid values.")
    return get_items(db, offset=offset, limit=limit)

