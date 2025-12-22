from pydantic import BaseModel
from typing import List


class BaseBlog(BaseModel):
    title: str
    body: str


class Blog(BaseBlog):
    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        from_attributes = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    class Config():
        from_attributes = True