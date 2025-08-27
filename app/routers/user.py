from typing import List
from fastapi import APIRouter, Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session
import models, schemas, utils
from db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.UserResponse) #Response for user creation
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = utils.hash(user.password) #hashingggg
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user