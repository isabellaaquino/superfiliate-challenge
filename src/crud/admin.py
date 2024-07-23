from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, get_db
from src.main import app
from src.database_models.config.rules import DiscountRule, ExcludedCollection
from src.schemas.config.rules import (CollectionDiscountConfig, DiscountRule as DiscountRuleSchema,
                                      ExcludedCollection as ExcludedCollectionSchema)


@app.get("/admin/config", response_model=CollectionDiscountConfig)
def get_config(db: Session = Depends(get_db)) -> CollectionDiscountConfig:
    excluded_collections = [ec.name for ec in db.query(ExcludedCollection).all()]
    discount_rule = db.query(DiscountRule).first()
    
    return CollectionDiscountConfig(excluded_collections=excluded_collections, discount_rules=discount_rules)


@app.post("/admin/config/discount_rule", response_model=DiscountRuleSchema)
def add_discount_rule(rule: DiscountRuleSchema, db: Session = Depends(get_db)):
    db_rule = DiscountRule(min_qty=rule.min_boxes, discount_percentage=rule.discount_percentage)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@app.post("/admin/config/excluded_collection", response_model=ExcludedCollectionSchema)
def add_excluded_collection(collection: ExcludedCollectionSchema, db: Session = Depends(get_db)):
    db_collection = ExcludedCollection(name=collection.name)
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection