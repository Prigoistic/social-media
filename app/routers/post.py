from typing import List
from fastapi import APIRouter, Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session
import models, schemas, utils
from db import get_db

#api router is just a way to group related endpoints

router = APIRouter()

@router.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

    # try:
    #     posts = db.execute("SELECT * FROM posts;").fetchall()
    #     return {"data": posts}
    # except Exception as e:
    #     print(f"Error fetching posts: {e}")
    #     raise HTTPException(status_code=500, detail="Failed to fetch posts from database")

@router.post("/createposts/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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

@router.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post not found", "status_code": status.HTTP_404_NOT_FOUND}
    db.delete(post)
    db.commit()
    return {"data": "Post deleted successfully"}
   


@router.put("/posts/{id}")
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