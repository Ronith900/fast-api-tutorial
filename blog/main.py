from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(engine)


app = FastAPI()


@app.post("/blogs",status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    print(f'received request body {blog}')
    db_blog = models.Blog(
        title=blog.title,
        body=blog.body
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog



@app.get("/blogs")
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int,db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'delted'


@app.get("/blogs/{id}",status_code=200)
def get(id:int,response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details':f"Blog with {id} not found in DB"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found in DB")
    return blog