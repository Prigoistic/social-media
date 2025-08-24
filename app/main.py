from urllib import response
from fastapi import FastAPI, Response, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import status
from passlib.context import CryptContext
import psycopg
from psycopg.rows import dict_row
import time
import db
import models, schemas  # Import models and schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from db import engine, get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)  # Create database tables

app = FastAPI()





# # Global variables for database connection
# conn = None
# cursor = None

# def get_db_connection():
#     """Get database connection with proper error handling"""
#     global conn, cursor
#     try:
#         if conn is None or conn.closed:
#             conn = psycopg.connect(
#                 host='localhost',
#                 dbname='fastapi',
#                 user='postgres',
#                 password='priyam@9753',
#                 port='5432'
#             )
#             print("Database connection was successful!")
#             cursor = conn.cursor(row_factory=dict_row)
#             print("Cursor created with dict_row support!")
#         return conn, cursor
#     except Exception as error:
#         print("Connecting to database failed")
#         print(f"Error: {error}")
#         raise HTTPException(status_code=500, detail="Database connection failed")

# # Initialize connection on startup
# try:
#     get_db_connection()
# except Exception as e:
#     print(f"Initial database connection failed: {e}")

# my_posts = [
#     {"title": "Post 1", "content": "Content of post 1", "published": True, "rating": 5, "id": 1},
#     {"title": "Post 2", "content": "Content of post 2", "published": False, "rating": 3, "id": 2},
#     {"title": "Post 3", "content": "Content of post 3", "published": True, "rating": 4, "id": 3}
# ]

@app.get("/")
def read_root():
    return {"message": "Welcome to the POST application!"}


#db: Session = Depends(get_db) this is a dependency injection 

@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

    # try:
    #     posts = db.execute("SELECT * FROM posts;").fetchall()
    #     return {"data": posts}
    # except Exception as e:
    #     print(f"Error fetching posts: {e}")
    #     raise HTTPException(status_code=500, detail="Failed to fetch posts from database")

@app.post("/createposts/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    # new_post = cursor.fetchone()
    # conn.commit() #commits changes into the database
    # post_dict = dict(new_post)
    # my_posts.append(post_dict)  # Append the new post to the in-memory list

    # return {"data": "Post created successfully", "post": post_dict}  

# @app.get("/posts/latest")   #here latest post is before the id cause we dont want latest to be confused with id as a path parameter
# def get_latest_post():
#     if my_posts:
#         latest_post = max(my_posts, key=lambda x: x['id'])
#         return {"data": latest_post}
#     return {"error": "No posts available", "status_code": 404}

@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}
    db.delete(post)
    db.commit()
    return {"data": "Post deleted successfully"}
   


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostUpdate, response: Response, db: Session = Depends(get_db)):
    update_data = post.model_dump(exclude_unset=True)
    update_data.pop("id", None)  # Remove 'id' if present
    updated = db.query(models.Post).filter(models.Post.id == id).update(update_data)
    db.commit()
    if not updated:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    return updated_post

# cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()  # Fetch the updated post from the database
    # conn.commit()  # Commit the changes to the database
    # if updated_post is None:  # If no post was updated, return an error
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}        
    # return {"data": "Post updated successfully", "updated_post": dict(updated_post)}

@app.post("/users/", response_model=schemas.UserResponse) #Response for user creation
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = pwd_context.hash(user.password) #hashingggg
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user