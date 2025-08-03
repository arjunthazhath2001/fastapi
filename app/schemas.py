from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content: str
    published:bool=True


# all our pydantic models has to extend the base model

# our request schema
class PostCreate(PostBase):
    pass


# our response schema
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True