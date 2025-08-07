from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import status
import psycopg
from psycopg.rows import dict_row

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: Optional[int] = None

# Global variables for database connection
conn = None
cursor = None

def get_db_connection():
    """Get database connection with proper error handling"""
    global conn, cursor
    try:
        if conn is None or conn.closed:
            conn = psycopg.connect(
                host='localhost',
                dbname='fastapi',
                user='postgres',
                password='priyam@9753',
                port='5432'
            )
            print("Database connection was successful!")
            cursor = conn.cursor(row_factory=dict_row)
            print("Cursor created with dict_row support!")
        return conn, cursor
    except Exception as error:
        print("Connecting to database failed")
        print(f"Error: {error}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Initialize connection on startup
try:
    get_db_connection()
except Exception as e:
    print(f"Initial database connection failed: {e}")

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
    try:
        conn, cursor = get_db_connection()
        cursor.execute("""SELECT * FROM posts;""")
        posts = cursor.fetchall()
        return {"data": posts}
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch posts from database")

@app.post("/createposts/", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    conn, cursor = get_db_connection()  # Ensure we have a valid connection FIRST
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit() #commits changes into the database
    post_dict = dict(new_post)
    my_posts.append(post_dict)  # Append the new post to the in-memory list

    return {"data": "Post created successfully", "post": post_dict}  

@app.get("/posts/latest")   #here latest post is before the id cause we dont want latest to be confused with id as a path parameter
def get_latest_post():
    if my_posts:
        latest_post = max(my_posts, key=lambda x: x['id'])
        return {"data": latest_post}
    return {"error": "No posts available", "status_code": 404}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (id,))
    post = cursor.fetchone()
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}
    return {"data": post}


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
