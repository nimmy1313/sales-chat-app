from fastapi import APIRouter,Depends
from security import get_current_user

my_orders_router=APIRouter()

@my_orders_router.get("/orders")
def get_orders(current_user_id:int=Depends(get_current_user)):
    return {"Message":"My orders","current_user_id":current_user_id}