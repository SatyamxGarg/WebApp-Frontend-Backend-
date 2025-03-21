from fastapi import APIRouter
from app.controllers import (
    auth,
    product,
    cart,
    order
)

root_api_router = APIRouter(prefix="/api/v1")

root_api_router.include_router(auth.router, prefix="/auth", tags=["AUTH ENDPOINTS"])
root_api_router.include_router(product.router, prefix="/product", tags=["PRODUCT ENDPOINTS"])
root_api_router.include_router(cart.router, prefix="/cart", tags=["CART ENDPOINTS"])
root_api_router.include_router(order.router, prefix="/order", tags=["ORDER ENDPOINTS"])

