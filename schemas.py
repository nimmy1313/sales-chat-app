from pydantic import BaseModel,EmailStr

class UserSignup(BaseModel):
    full_name:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class CreateProduct(BaseModel):
    title:str
    category:str
    description:str
    price:float
    current_stock:int
    