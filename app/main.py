from typing import Optional
from fastapi import FastAPI,status, HTTPException,Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db



models.Base.metadata.create_all(bind=engine)



app= FastAPI()




class Post(BaseModel):
    title:str
    content: str
    published:bool=True
    rating: Optional[int]= None


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



@app.get("/")
def root():
    return {"message":"hi world"}


@app.get("/sql")
def testing(db: Session=Depends(get_db)):
        posts= db.query(models.Post).all()
        return {"message":posts}


#get all posts
@app.get('/posts')
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts=cursor.fetchall()
    return {'posts':posts}


#get latest post
@app.get('/posts/latest')
async def latest_post():
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    new_posts=cursor.fetchall()
    return new_posts

#get specific post
@app.get('/posts/{id}')
async def get_post(id:int):  
    try:
        cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
        post=cursor.fetchone()
        return {"result":post}
    except: 
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
  
#create a post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post:Post):
    try:
        cursor.execute("INSERT INTO posts(title,content,published) VALUES(%s,%s,%s)RETURNING *",(post.title,post.content,post.published))
        new_post=cursor.fetchone()
        conn.commit()
        return {"message":f"post created: {new_post}"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="couldn't create")



#delete a post
@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):

    cursor.execute("DELETE FROM posts where id=%s RETURNING *",(str(id),))
    deleted_post= cursor.fetchone()
    conn.commit()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    else:
        return {"deleted":deleted_post}  


@app.patch('/posts/{id}',status_code=status.HTTP_200_OK)
async def update_post(id:int,p:Post):
    cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *",(p.title,p.content,p.published,str(id)))
    updated_post=cursor.fetchone()

    conn.commit()
    
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")

    return {"updated post":updated_post}