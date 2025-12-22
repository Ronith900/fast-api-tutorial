from typing import List
from .. import schemas,models
from ..database import engine,get_db
from fastapi import Depends, status, Response, HTTPException, APIRouter

from ..repository import blog

from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)


@router.post("/",status_code=status.HTTP_201_CREATED)
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



@router.get("/",response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.show_all(db)


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id:int, request:schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'Updated'


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def delete(id:int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} not found')    
    blog.delete(synchronize_session=False)
    db.commit()
    return 'delted'

@router.get("/{id}",status_code=200,response_model=schemas.ShowBlog,tags=['blogs'])
def get(id:int,response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found in DB")
    return blog