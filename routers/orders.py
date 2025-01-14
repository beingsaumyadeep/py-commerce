# routers/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create order
    db_order = models.Order(user_id=order.user_id, status="pending")
    db.add(db_order)
    db.flush()

    # Add order items
    total_amount = 0
    for item in order.items:
        product = (
            db.query(models.Product)
            .filter(models.Product.id == item.product_id)
            .first()
        )
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product {item.product_id} not found"
            )

        # Check stock
        stock = (
            db.query(models.ProductStock)
            .filter(models.ProductStock.product_id == item.product_id)
            .first()
        )
        if stock.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {item.product_id}",
            )

        # Create order item
        order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_time=product.price,
        )
        db.add(order_item)

        # Update stock
        stock.quantity -= item.quantity
        total_amount += product.price * item.quantity

    # Create transaction
    transaction = models.Transaction(
        order_id=db_order.id,
        amount=total_amount,
        status="pending",
        payment_method="credit_card",  # This would normally come from the request
    )
    db.add(transaction)

    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders
