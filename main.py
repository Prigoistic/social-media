from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: Optional[int] = None

my_posts = [
    {"title": "Post 1", "content": "Content of post 1", "published": True, "rating": 5, "id": 1},
    {"title": "Post 2", "content": "Content of post 2", "published": False, "rating": 3, "id": 2},
    {"title": "Post 3", "content": "Content of post 3", "published": True, "rating": 4, "id": 3}
]

@app.get("/")
def read_root():
    return {"message": "Welcome to the POST application!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/createposts/")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": "Post created successfully", "post": post_dict}  
