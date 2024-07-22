from sqlalchemy import Column, String, TIMESTAMP, Float, PrimaryKeyConstraint, orm
from src.database import Base


class CartItem(Base):
    __tablename__ = "cart_item"

    name = Column(String, nullable=False)
    price = Column(Float(precision=2), nullable=False)
    collection = Column(String, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("name", "collection"),)

    @orm.validates('price')
    def validate_price(self, key, value):
        if not 0 < value:
            raise ValueError(f'Price should be bigger than 0. Given value {value}.')
        return value
