from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # This enables ORM mode
        # Use this to configure the model further if needed

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase): #this class is the respone we send back the user and we dont want the user the see the password ofc 
    created_at: datetime
    id: int 

    class Config:
        from_attributes = True
    created_at: datetime
    id: int

    class Config:
        from_attributes = True  # This enables ORM mode
        # Use this to configure the model further if needed
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
