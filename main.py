from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {'data':{'name':"Ronith N"}}


@app.get("/about")
def about():
    return {'data':{'app':"Promola Application"}}
