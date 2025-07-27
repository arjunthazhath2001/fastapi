from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import uuid
import psycopg2

app= FastAPI()

class Post(BaseModel):
    title:str
    content: str
    published:bool=True
    rating: Optional[int]= None


try:
    conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
except:
    print("I am unable to connect to the database")



mypost=[{"id":uuid.uuid4(),"title":"hello world","content":"how things going?"},{"id":"2","title":"hello world2","content":"how things going?2"}]

#get all posts
@app.get('/posts')
async def get_posts():
    return {'posts':mypost}


#get latest post
@app.get('/posts/latest')
async def latest_post():
    return mypost[-1]

#get specific post
@app.get('/posts/{id}')
async def get_post(id:str):  
    for p in mypost:
        if id==p["id"]:
            return {"result":p}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
  
#create a post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post:Post):
    newpost=post.dict()
    try:
        newpost["id"]= str(uuid.uuid4())
        mypost.append(newpost)
        return {"message":"post created"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="couldn't create")



#delete a post
@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:str):
    
    for i,post in enumerate(mypost):
        if post["id"]==id:
            mypost.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")



@app.patch('/posts/{id}',status_code=status.HTTP_200_OK)
async def update_post(id:str,p:Post):
    for i,post in enumerate(mypost):
        if post["id"]==id:
            post["title"]=p.title
            post["content"]=p.content
            return {"messg":"updated"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
    