
from sqlalchemy.orm import Session
from .. import models,schemas
from ..database import get_db
from pwdlib import PasswordHash


from fastapi import Depends, HTTPException,status

password_hash = PasswordHash.recommended()

def create_user(request: schemas.User,db: Session = Depends(get_db)):
    hash_pw = password_hash.hash(request.password)
    new_user = models.User(name=request.name.title(),email=request.email,password=hash_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


def get(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found in DB")
    return user