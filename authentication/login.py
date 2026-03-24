from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from utils import verify_pass 
from database_models import User
from oauth import create_token


router = APIRouter(tags=["login"])

@router.post("/login")
def login(uc:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == uc.username) | (User.email == uc.username)).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email")
    
    if not verify_pass(uc.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    # return token.
    payload = {"user_id":db_user.id}
    access_token = create_token(payload)
    return {"access_token":access_token, "token_type":"bearer"}



























