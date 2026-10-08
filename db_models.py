from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database_connection import engine

Base=declarative_base()

class User(Base):
    __tablename__="users"
    user_id=Column(Integer,primary_key=True,index=True)
    full_name=Column(String,index=True)
    email=Column(String,unique=True,index=True)
    password_hash=Column(String)
    chathistory=relationship("Chathistory",back_populates="user")

class Product(Base):
    __tablename__="products"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True)
    category=Column(String,index=True)
    description=Column(String)
    price=Column(Integer)
    current_stock=Column(Integer)
    created_at=Column(DateTime,default=datetime.now)

class Chathistory(Base):
    __tablename__="chathistory"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.user_id"),index=True)
    sender=Column(String,index=True)
    message=Column(String)
    timestamp=Column(DateTime,default=datetime.now)
    user=relationship("User",back_populates="chathistory")

Base.metadata.create_all(bind=engine)