import jwt
from typing import Optional
from datetime import datetime, timedelta
import pytz
from settings import configs as conf
from auth import schemas


def verify_password(plain_password: str, hashed_password: str):
    return conf.PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return conf.PWD_CONTEXT.hash(password)


def add_access_token(token_data: schemas.TokenData) -> bytes:
    to_encode = token_data.dict()
    expire = datetime.utcnow() + timedelta(minutes=conf.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    data = schemas.TokenFullData(**to_encode)
    encoded_jwt = jwt.encode(data.dict(), conf.SECRET_KEY, algorithm=conf.JWT_ALGORITHM)
    return encoded_jwt


def validate_access_token(access_token: str):
    payload = jwt.decode(access_token, conf.SECRET_KEY, algorithms=[conf.JWT_ALGORITHM])
    token_full_data = schemas.TokenFullData(**payload)
    if token_full_data.exp >= datetime.now((pytz.utc)):
        return payload
