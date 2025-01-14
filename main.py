from fastapi import FastAPI
from sqlalchemy.orm import Session
from typing import List
import models

# import schemas
import uvicorn
from database import engine
from routers import users, products, orders


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API")

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
