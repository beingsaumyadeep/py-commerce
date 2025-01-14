from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True
        
        



class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductMetadataBase(BaseModel):
    brand: str
    category: str
    specifications: Dict


class ProductMetadataCreate(ProductMetadataBase):
    pass


class ProductMetadata(ProductMetadataBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class ProductStock(BaseModel):
    quantity: int
    last_updated: datetime

    class Config:
        from_attributes = True


class Product(ProductBase):
    id: int
    created_at: datetime
    metadata: Optional[ProductMetadata]
    stock: Optional[ProductStock]

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    price_at_time: float

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: int


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    status: str
    created_at: datetime
    items: List[OrderItem]

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    amount: float
    payment_method: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    order_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AIGen(BaseModel):
    command: str