from jose import JWTError,jwt
from datetime import datetime,timedelta
import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
    


#secret key
#algorithm hs256
#expiration time


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

def verify_token(token:str, credentials_exception):
    try:
        print(f"Attempting to decode token: {token[:20]}...")  # Only print first 20 chars for security
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Token payload: {payload}")
        id: str = payload.get("sub")
        print(f"Extracted user ID: {id}")
        if id is None:
            print("No 'sub' claim found in token")
            raise credentials_exception
        token_data = schemas.TokenData(id=id) #token_data is an instance of TokenData which basically just holds the user id and the schema makes sure it's valid
        print(f"Token validation successful for user ID: {id}")
        return token_data
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception

def get_current_user(token : str = Depends(oauth2_scheme)):
    print(f"get_current_user called with token: {token[:20] if token else 'None'}...")
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_token(token, credential_exception)