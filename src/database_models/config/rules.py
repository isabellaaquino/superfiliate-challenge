from sqlalchemy import Column, Integer, String, Float
from src.database import Base


class DiscountRule(Base):
    __tablename__ = 'discount_rules'
    id = Column(Integer, primary_key=True, index=True)
    min_qty = Column(Integer, nullable=False)
    discount_percentage = Column(Float, nullable=False)


class ExcludedCollection(Base):
    __tablename__ = 'excluded_collections'
    id = Column(Integer, primary_key=True, index=True)
    collection = Column(String, nullable=False)
