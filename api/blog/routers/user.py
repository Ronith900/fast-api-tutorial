from typing import List
from .. import schemas,models
from ..database import engine,get_db
from fastapi import Depends, status, HTTPException, APIRouter
from ..repository import user

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/user",
    tags=['users']
)



@router.post("/",status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User,db: Session = Depends(get_db)):
    return user.create_user(request,db)

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser])
def get_users(db: Session = Depends(get_db)):
    return user.get_users(db)


@router.get("/{id}",status_code=200,response_model=schemas.ShowUser,tags=['users'])
def get(id:int, db: Session = Depends(get_db)):
    return user.get(id,db)