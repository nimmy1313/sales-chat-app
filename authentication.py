from fastapi import APIRouter,Depends,HTTPException,status
from schemas import UserSignup,UserLogin
from database_connection import get_db
from db_models import User
from security import hash_password,verify_password,generate_token

authentication_router=APIRouter(prefix="/api/auth",tags=['Authentication'])

@authentication_router.post("/signup")
def signup(request:UserSignup,db=Depends(get_db)):
    hashed_password=hash_password(request.password)
    user=db.query(User).filter(User.email==request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")
    new_user=User(full_name=request.full_name,email=request.email,password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    return {"status":"Success","code":200,"Message":"User Successfully created"}

@authentication_router.post("/login")
def login(request:UserLogin,db=Depends(get_db)):
    user=db.query(User).filter(User.email==request.email).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Wrong email or password")
    does_password_match=verify_password(request.password,user.password_hash)
    if does_password_match==False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Wrong email or password")
    jwt_token=generate_token(user.user_id)
    return {"Status":"Success","code":200,"Message":"Login successful","Token":jwt_token}


