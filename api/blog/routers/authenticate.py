from fastapi import APIRouter,status,Depends, HTTPException
from .. import schemas, models, token
from fastapi.security import  OAuth2PasswordRequestForm
from ..database import engine,get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=['login'])



@router.post("/login",status_code=status.HTTP_201_CREATED)
def login(request:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = token.authenticate_user(db,request)
    print(f"login route - {request} for {user.id}")
    access_token = token.create_access_token(data={"sub": f'{user.id}'})
    return access_token