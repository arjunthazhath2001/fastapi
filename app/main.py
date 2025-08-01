from typing import Optional
from fastapi import FastAPI,status, HTTPException,Depends,Response
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
        print(posts)
        return {"message":"success"}


#get all posts
@app.get('/posts')
async def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts=cursor.fetchall()
    posts= db.query(models.Post).all()
    return {'posts':posts}


#get latest post
@app.get('/posts/latest')
async def latest_post():
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    new_posts=cursor.fetchall()
    return new_posts

#get specific post
@app.get('/posts/{id}')
async def get_post(id:int,db:Session=Depends(get_db)):  
    try:
        # cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
        # post=cursor.fetchone()
        post=db.query(models.Post).filter(models.Post.id==id).first()
        return {"result":post}
    except: 
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
  
#create a post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post:Post,db: Session=Depends(get_db)):
    try:
        # cursor.execute("INSERT INTO posts(title,content,published) VALUES(%s,%s,%s)RETURNING *",(post.title,post.content,post.published))
        # new_post=cursor.fetchone()
        # conn.commit()

        new_post=models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"message":f"post created: {new_post}"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"couldn't create: {str(e)}")




#delete a post
@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session=Depends(get_db)):

    # cursor.execute("DELETE FROM posts where id=%s RETURNING *",(str(id),))
    # deleted_post= cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)

    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    else:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.patch('/posts/{id}',status_code=status.HTTP_200_OK)
async def update_post(id:int,updated_post:Post,db:Session=Depends(get_db)):
    # cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *",(p.title,p.content,p.published,str(id)))
    # updated_post=cursor.fetchone()

    # conn.commit()
    post= db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    else:
        new_post=post.update(updated_post.dict(),synchronize_session=False)
        db.commit()
    return {"updated post":new_post}