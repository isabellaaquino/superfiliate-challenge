from sqlalchemy import Column, String, Float, PrimaryKeyConstraint, orm, Integer
from src.database import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float(precision=2), nullable=False)
    collection = Column(String, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("name", "collection"),)

    @orm.validates('price')
    def validate_price(self, key, value):
        if not 0 < value:
            raise ValueError(f'Price should be bigger than 0. Given value {value}.')
        if len(str(value)) > 10:
            raise ValueError(f'Price can have up to 10 maximum digits. Given value {value}.')
        return value
