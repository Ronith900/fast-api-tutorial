
from sqlalchemy.orm import Session
from .. import models,schemas
from ..database import get_db

from fastapi import Depends, HTTPException,status




def show_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session = Depends(get_db)):
    print(f'received request body {request}')
    db_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update(id:int, request:schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'Updated'


def delete(id:int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} not found')    
    blog.delete(synchronize_session=False)
    db.commit()
    return 'delted'

def get(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found in DB")
    return blog