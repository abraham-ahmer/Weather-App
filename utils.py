#hashing the password for secure signup
from passlib.context import CryptContext

secure = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(plain_password:str)->str:
    return secure.hash(plain_password)

def verify_pass(plain_password:str, hashed_password:str)->bool:
    return secure.verify(plain_password, hashed_password)












