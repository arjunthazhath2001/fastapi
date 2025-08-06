from typing import Optional
from fastapi import FastAPI,status, HTTPException,Depends,Response
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas
from sqlalchemy.orm import Session
from .database import engine, get_db

from .utils import hash
from .routers import post,user,auth

models.Base.metadata.create_all(bind=engine)


app= FastAPI()




while True:
    try:
        conn = psycopg2.connect(dbname='fastapi', user='postgres' ,host='localhost', password='arjunomia',cursor_factory=RealDictCursor)
        cursor= conn.cursor()
        print("🦄🦄🦄🦄🦄🦄Connection success🦄🦄🦄🦄🦄")
        break
    except Exception as error:
        print("❌❌❌❌❌I am unable to connect to the database❌❌❌❌❌")
        print(error)
        time.sleep(2)



app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message":"hi world"}








