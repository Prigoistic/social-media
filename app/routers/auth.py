from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

import schemas, models, utils
from db import get_db

router = APIRouter(tags=["Auth"])

@router.post('/login', response_model=schemas.UserResponse)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
   if not user or not utils.verify_password(user_credentials.password, user.password):
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
   return user


