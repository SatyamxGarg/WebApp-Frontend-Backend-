from . import TimestampMixin
from mongoengine import Document, ReferenceField, ListField
from .user import User
from .product import Product


class Wishlist(Document, TimestampMixin):
    meta = {'collection': 'wishlist'}
        
    user = ReferenceField(User, required=True, unique=True)
    products = ListField(ReferenceField(Product))