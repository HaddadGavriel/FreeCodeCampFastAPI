from typing import List
from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from . import schemas
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


