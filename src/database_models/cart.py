from sqlalchemy import Column, String, TIMESTAMP, Float, PrimaryKeyConstraint, orm, Integer
from src.database import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, nullable=False)