from urllib import response
from fastapi import FastAPI, Response, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import status
import psycopg
from psycopg.rows import dict_row
import time
import db
import models
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from db import engine, get_db


models.Base.metadata.create_all(bind=engine)  # Create database tables

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: Optional[int] = None

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

@app.get("/sqlalchemy") #test
def get_sqlalchemy_status(db: Session = Depends(get_db)):

    p = db.query(models.Post).all()
    return {"data": p}
#db: Session = Depends(get_db) this is a dependency injection 

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

    # try:
    #     posts = db.execute("SELECT * FROM posts;").fetchall()
    #     return {"data": posts}
    # except Exception as e:
    #     print(f"Error fetching posts: {e}")
    #     raise HTTPException(status_code=500, detail="Failed to fetch posts from database")

@app.post("/createposts/", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post( **post.model_dump()) # basically using spread operator
        # title=post.title,
        # content=post.content,
        # published=post.published,
        # rating=post.rating
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

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
    return {"data": post}


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
def update_post(id: int, post: Post, response: Response, db: Session = Depends(get_db)):
    existing_post = db.query(models.Post).filter(models.Post.id == id).first()
    if existing_post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}
    db.query(models.Post).filter(models.Post.id == id).update(post.model_dump())
    db.commit()
    return {"data": "Post updated successfully"}    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()  # Fetch the updated post from the database
    # conn.commit()  # Commit the changes to the database
    # if updated_post is None:  # If no post was updated, return an error
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}        
    # return {"data": "Post updated successfully", "updated_post": dict(updated_post)}

