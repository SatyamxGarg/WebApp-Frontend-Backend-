from app.models.cart import Cart
from app.schemas.cart import CartResponse
from app.models_2_schemas.user import create_user_response
from app.models_2_schemas.product import create_product_response


def create_cart_response(cart: Cart) -> CartResponse :
    return CartResponse(
        id=str(cart.id),
        user=create_user_response(cart.user),
        product = create_product_response(cart.product),
        quantity = cart.quantity,
        created_at=str(cart.created_at),
        updated_at=str(cart.updated_at)
    )