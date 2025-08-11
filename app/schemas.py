from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from email_validator import EmailStr


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

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(UserCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # This enables ORM mode
        # Use this to configure the model further if needed
