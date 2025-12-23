from pwdlib import PasswordHash
from fastapi import HTTPException,status,Depends
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta,datetime
from . import models,schemas
from sqlalchemy.orm import Session
from .database import engine,get_db


password_hash = PasswordHash.recommended()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def authenticate_user(db:Session,request:schemas.Login):
    #get user from db
    user_obj = db.query(models.User).filter(models.User.email == request.username).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='invalid credentials')
    if not verify_password(request.password,user_obj.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='invalid password')
    return user_obj

def create_access_token(data: dict):
    to_encode = data.copy()
    access_token_expires = datetime.utcnow() +  timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": access_token_expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return schemas.Token(access_token=encoded_jwt, token_type="bearer")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)):
    print(f'user token - {token}')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if isinstance(user_id,str):
            user_id = int(user_id)
        if user_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(user_id=user_id)
        return token_data
    except InvalidTokenError:
        raise credentials_exception
