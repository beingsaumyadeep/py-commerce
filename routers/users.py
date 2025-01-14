import os
from typing import List
import json
import secrets
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from anthropic import Anthropic
import models
import schemas
from database import get_db
from utils import get_current_user, get_password_hash, verify_password, redis_client


router = APIRouter(prefix="/users", tags=["users"])

client = Anthropic(
    api_key=os.environ.get("ANTROPIC_API"),  # This is the default and can be omitted
)

oauth2_scheme = HTTPBearer(scheme_name="Bearer")


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[schemas.User])
def read_users(start: int = 0, end: int = 10, db: Session = Depends(get_db)):
    """Retrieve a list of users from the database.

    Args:
        start (int): The number of records to skip. Defaults to 0.
        end (int): The maximum number of records to return. Defaults to 10.
        db (Session): The database session.

    Returns:
        List[schemas.User]: A list of user records.
    """
    users = db.query(models.User).offset(start).limit(end).all()
    return users


@router.get("/me")
def read_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    print(token)

    email = get_current_user(token)
    return db.query(models.User).filter(models.User.email == email).first()


@router.post("/generate")
def generate_with_claude_AI(b: schemas.AIGen):
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"${b.command}, Write it in JSON format and no words",
            }
        ],
        model="claude-3-5-haiku-latest",
    )
    json_compatible_item_data = jsonable_encoder(json.loads(message.content[0].text))
    return JSONResponse(content=json_compatible_item_data)


@router.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
async def login(
    user: schemas.UserLogin, request: Request, db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    user_agent = request.headers.get("user-agent")
    user_ip = request.client.host
    print(user_agent, user_ip)
    token = secrets.token_hex(16)
    redis_client.set(token, db_user.email, ex=60 * 60 * 24 * 15)
    if db_user and verify_password(user.password, db_user.hashed_password):
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=400, detail="Invalid credentials")
