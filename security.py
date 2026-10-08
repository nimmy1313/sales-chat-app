from argon2 import PasswordHasher
import jwt
from typing import Optional
from fastapi import Header,HTTPException,status

ph=PasswordHasher()
SECRET_KEY="hjdjdywuyxnsjdksudisddjhustyrstrydsdyutsudysjdh"

def hash_password(password:str)->str:
    return ph.hash(password)

def verify_password(password:str,hashed_password:str)->bool:
    try:
        return ph.verify(hashed_password,password)
    except:
        return False
    
def generate_token(user_id:int)->str:
    payload={"user_id":user_id}
    return jwt.encode(payload,SECRET_KEY,algorithm="HS256")

def verify_token(token:str)->int:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return payload["user_id"]
    except:
        return None

def get_current_user(authorization:Optional[str]=Header(None))->int:
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    parts=authorization.split()
    if len(parts)!=2 or parts[0].lower()!="bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication scheme")
    token=parts[1]
    # if not authorization.startswith("Bearer"):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication scheme")
    # scheme,token=authorization.split()
    # if scheme.lower()!="bearer":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Authentication scheme")
    current_user_id=verify_token(token)
    if current_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    return current_user_id

    
