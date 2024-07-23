from typing import List

from sqlalchemy.orm import Session

from src.database_models.item import Item


class ItemFetchException(Exception):
    message = "There is no equipment with the given id."


def create_item(db: Session, item: Item) -> Item:
    """
    Create a new equipment

    Args:
        db (Session): Database session.
        item (Item): Item sent from request

    Returns:
        Item: Created equipment.
    """
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item: Item) -> Item:
    """
    Retrieve an item from the database

    Args:
        db (Session): Database session.
        item (Item): Equipment sent from request

    Returns:
        list[Item]: List of equipments.
    """
    return db.query(Item).filter(Item.name == item.name).filter(Item.collection == item.collection).first()


def get_items(db: Session, offset: int = 0, limit: int = 100) -> List[Item]:
    """
    List all equipments.

    Args:
        db (Session): Database session.
        offset (int): Offset to start the list.
        limit (int): Limit of equipments to be listed.

    Returns:
        list[Item]: List of equipments.
    """
    return db.query(Item).offset(offset).limit(limit).all()
