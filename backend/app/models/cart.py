from . import TimestampMixin
from mongoengine import Document, ReferenceField, IntField
from .user import User
from .product import Product

class Cart(Document, TimestampMixin):
    meta = {'collection': 'cart'}  # Specifies the collection name
    
    user = ReferenceField(User, required=True)
    product = ReferenceField(Product, required=True)
    quantity = IntField(default=1)