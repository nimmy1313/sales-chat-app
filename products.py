from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import session
from security import get_current_user
from database_connection import get_db
from db_models import Product
from schemas import CreateProduct

products_router=APIRouter(prefix="/api",tags=["products"])

@products_router.get("/products")
async def get_all_products(current_user_id:int=Depends(get_current_user),db:session=Depends(get_db)):
    products=db.query(Product).all()
    return {"products":products}

@products_router.post("/products")
async def create_product(product:CreateProduct,current_user_id:int=Depends(get_current_user),db:session=Depends(get_db)):
    new_product=Product(title=product.title,category=product.category,description=product.description,price=product.price,current_stock=product.current_stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"product":new_product}