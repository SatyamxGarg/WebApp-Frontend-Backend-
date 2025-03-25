from . import TimestampMixin
from mongoengine import Document, ReferenceField, IntField, StringField
from .user import User
from .product import Product


class Review(Document, TimestampMixin):
    meta = {'collection': 'review'}
     
    user = ReferenceField(User, required=True)
    product = ReferenceField(Product, required=True)
    rating = IntField(min_value=1, max_value=5, required=True)
    review_text = StringField(max_length=100)
