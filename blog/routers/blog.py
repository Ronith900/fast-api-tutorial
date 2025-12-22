from typing import List
from .. import schemas
from ..database import engine,get_db
from fastapi import Depends, status, Response, APIRouter

from ..repository import blog

from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request,db)



@router.get("/",response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.show_all(db)


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id:int, request:schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id,request,db)


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def delete(id:int,db: Session = Depends(get_db)):
    return blog.delete(id,db)

@router.get("/{id}",status_code=200,response_model=schemas.ShowBlog,tags=['blogs'])
def get(id:int,response: Response, db: Session = Depends(get_db)):
    return blog.get(id,db)