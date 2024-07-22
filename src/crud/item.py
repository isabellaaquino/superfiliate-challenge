from sqlalchemy.orm import Session

from src.database_models.item import Item


class ItemFetchException(Exception):
    message = "There is no equipment with the given id."


def create_cart_item(db: Session, cart_item: Item) -> Item:
    """
    Create a new equipment

    Args:
        db (Session): Database session.
        cart_item (Item): Equipment sent from request

    Returns:
        Item: Created equipment.
    """
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def get_cart_items(db: Session, offset: int = 0, limit: int = 100) -> list[Item]:
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
