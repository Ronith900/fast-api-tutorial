from typing import Union,Optional


from fastapi import FastAPI
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


app = FastAPI()


@app.post("/blog")
def create_blog(blog: Blog):
    print("Blog cretaed")
    return {'data':f'blog created with title {blog.title}'}

@app.get("/blog/")
def index(limit:int =10,published: bool = True,sort: Optional[str]=None):
    if published:
        return {'data':f'{limit} published blogs from db'}
    else:
        return {'data':f'{limit} unpublished blogs from db'}


@app.get('/blog/unpublished')
def unpublished():
    # fetch blogs with id
    return {'data':"Unpublished posts"}


@app.get('/blog/{id}')
def show(id: int):
    # fetch blogs with id
    return {'data':id}



@app.get("/blog/{id}/comments")
def blog_comments(id:int):
    return {'data':{'comments':[1,2,3,4]}}