from typing import List
from .. import schemas,models
from ..database import engine,get_db
from fastapi import Depends, status, HTTPException, APIRouter
from pwdlib import PasswordHash

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/user",
    tags=['users']
)


password_hash = PasswordHash.recommended()

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User,db: Session = Depends(get_db)):
    hash_pw = password_hash.hash(request.password)
    new_user = models.User(name=request.name.title(),email=request.email,password=hash_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}",status_code=200,response_model=schemas.ShowUser,tags=['users'])
def get(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found in DB")
    return user