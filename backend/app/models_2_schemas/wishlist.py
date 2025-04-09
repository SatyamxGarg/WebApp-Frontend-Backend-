from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistResponse
from app.models_2_schemas.user import create_user_response
from app.models_2_schemas.product import create_product_response


def create_wishlist_response(wishlist: Wishlist) -> WishlistResponse:
    return WishlistResponse(
         id = str(wishlist.id),
         user = create_user_response(wishlist.user),
         products = [create_product_response(product) for product in wishlist.products],
         created_at = wishlist.created_at,
         updated_at = wishlist.updated_at
    )