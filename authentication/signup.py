from fastapi import APIRouter, Depends, HTTPException
from models import UserCreate, UserResponse
from database_models import User
from database import get_db
from sqlalchemy.orm import Session
from utils import hash_pass

router = APIRouter(tags=["Signup"])

@router.post("/signup", response_model=UserResponse)
def signup(uc:UserCreate, db:Session = Depends(get_db)):

    user = db.query(User).filter(User.email == uc.email).first()

    if user:
        raise HTTPException(status_code=401, detail="User already exist")

    hashed_pass = hash_pass(uc.password)
    uc.password = hashed_pass

    new_user = User(**uc.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user














