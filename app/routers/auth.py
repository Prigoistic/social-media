from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import schemas, models, utils, outh2
from db import get_db

router = APIRouter(tags=["Auth"])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #username,password
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    access_token = outh2.create_access_token(data={"sub": str(user.id)})
    print(f"Created access token for user {user.id}: {access_token[:20]}...")
    return {"access_token": access_token, "token_type": "bearer"}



