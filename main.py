from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import uuid

app= FastAPI()

class Post(BaseModel):
    title:str
    content: str
    published:bool=True
    rating: Optional[int]= None


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
@app.get('/post/{id}')
async def get_post(id:str):  
    for p in mypost:
        if id==p["id"]:
            return {"result":p}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
  
#create a post
@app.post('/posts')
async def create_posts(post:Post):
    newpost=post.dict()
    newpost["id"]= str(uuid.uuid4())
    mypost.append(newpost)
    return {"message":"post created"}


