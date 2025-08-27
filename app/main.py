from urllib import response
from fastapi import FastAPI, Response, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import status
import utils
import psycopg
from psycopg.rows import dict_row
import time
import db
import models, schemas  # Import models and schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from db import engine, get_db
from routers import post, user


models.Base.metadata.create_all(bind=engine)  # Create database tables

app = FastAPI()

app.include_router(post.router, prefix="/posts", tags=["Posts"])
app.include_router(user.router, prefix="/users", tags=["Users"])

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



