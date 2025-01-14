import os
from passlib.context import CryptContext
from fastapi import Security, HTTPException
from fastapi.security import OAuth2PasswordBearer
import redis

# from jwt import PyJWTError

pwd_context = CryptContext(schemes=["sha256_crypt", "des_crypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    username=os.environ.get("REDIS_USER"),
    password=os.environ.get("REDIS_PASS"),
    ssl=True
)


def get_current_user(token: str):
    email = redis_client.get(token)
    print(email)
    if email is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return email.decode("utf-8")
