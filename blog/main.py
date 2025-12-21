from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine,get_db
from sqlalchemy.orm import Session
from pwdlib import PasswordHash


models.Base.metadata.create_all(engine)


app = FastAPI()


@app.post("/blogs",status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    print(f'received request body {request}')
    db_blog = models.Blog(
        title=request.title,
        body=request.body
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog



@app.get("/blogs",response_model=List[schemas.ShowBlog],tags=['blogs'])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id:int, request:schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'Updated'


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def delete(id:int,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} not found')    
    blog.delete(synchronize_session=False)
    db.commit()
    return 'delted'

@app.get("/blogs/{id}",status_code=200,response_model=schemas.ShowBlog,tags=['blogs'])
def get(id:int,response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found in DB")
    return blog

password_hash = PasswordHash.recommended()

@app.post("/users",status_code=status.HTTP_201_CREATED,tags=['users'])
def create_user(request: schemas.User,db: Session = Depends(get_db)):
    hash_pw = password_hash.hash(request.password)
    new_user = models.User(name=request.name.title(),email=request.email,password=hash_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser],tags=['users'])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/users/{id}",status_code=200,response_model=schemas.ShowUser,tags=['users'])
def get(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"User with {id} not found in DB")
    return user