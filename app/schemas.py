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
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


