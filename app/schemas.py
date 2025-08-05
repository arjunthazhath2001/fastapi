from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content: str
    published:bool=True


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str


# all our pydantic models has to extend the base model

# our request schema
class PostCreate(PostBase):
    pass


class UserCreate(UserBase):
    pass

# our response schema
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True



class User(UserBase):
    pass


class UserOut(BaseModel):
    id:int
    email: EmailStr
    
    class Config:
        orm_mode= True


class UserLogin(BaseModel):
    email: EmailStr
    password:str