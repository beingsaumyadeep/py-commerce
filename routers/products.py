# routers/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    metadata: schemas.ProductMetadataCreate,
    stock: int,
    db: Session = Depends(get_db),
):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.flush()

    db_metadata = models.ProductMetadata(**metadata.dict(), product_id=db_product.id)
    db_stock = models.ProductStock(product_id=db_product.id, quantity=stock)

    db.add(db_metadata)
    db.add(db_stock)
    db.commit()
    db.refresh(db_product)

    return db_product


@router.get("/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products
