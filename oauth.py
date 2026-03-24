from jose import JWTError, jwt
from datetime import datetime, timedelta
from models import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from database import get_db
from database_models import User
from sqlalchemy.orm import Session

SECRET_KEY = "asecureandsecretkey"
ALGORITHM = "HS256"
EXPIRATION_TIME = 30

def create_token(data:dict):
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp":expiry})
    jwt_token = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token



def verify_token(token:str, credential_exception):
    try:
        decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        us_id = decoded_token.get("user_id")

        if not us_id:
            raise credential_exception
        return TokenData(id=us_id)
    
    except JWTError:
        raise credential_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def allow_access(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "User deleted or not exist",
        headers= {"WWW-Authenticate": "bearer"}
    )

    new_token = verify_token(token, credential_exception)
    user_query = db.query(User).filter(User.id == new_token.id).first()

    if not user_query:
        raise credential_exception
    return user_query

























