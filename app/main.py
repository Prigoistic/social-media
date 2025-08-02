from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import status

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

@app.post("/createposts/", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": "Post created successfully", "post": post_dict}  

@app.get("/posts/latest")   #here latest post is before the id cause we dont want latest to be confused with id as a path parameter
def get_latest_post():
    if my_posts:
        latest_post = max(my_posts, key=lambda x: x['id'])
        return {"data": latest_post}
    return {"error": "No posts available", "status_code": 404}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    for post in my_posts:
        if post['id'] == id:
            return {"data": post}
    response.status_code = status.HTTP_404_NOT_FOUND

    return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    for index, post in enumerate(my_posts): # enumerate gives us both index and post
        if post['id'] == id: # Check if the post ID matches
            del my_posts[index]     # Delete the post from the list
            return Response(status_code=status.HTTP_204_NO_CONTENT) # Return 204 No Content 
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}

@app.put("/posts/{id}")
def update_post(id: int, post: Post, response: Response):
    for index, existing_post in enumerate(my_posts): # enumerate gives us both index and existing_post
        if existing_post['id'] == id:
            post_dict = post.model_dump()   # Convert Pydantic model to dict
            post_dict['id'] = id # Ensure the ID remains the same
            my_posts[index] = post_dict # Update the post in the list
            return {"data": post_dict}  # Return the updated post
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}
