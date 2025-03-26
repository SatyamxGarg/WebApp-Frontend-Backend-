from mongoengine import Document, StringField, IntField, FloatField, ReferenceField
from . import TimestampMixin
from app.models.subcategory import Subcategory

class Product(Document, TimestampMixin):
    meta = {'collection': 'products'}  # Specifies the collection name
    
    product_name = StringField(required=True)
    product_id = StringField(required=True, Unique=True)
    product_description = StringField()
    product_price = FloatField(required=True)
    product_stock = IntField(default=0)
    product_rating = FloatField(default=0.0)
    # images = ListField(StringField())  # Store image URLs
    subcategory = ReferenceField(Subcategory, required=True, reverse_delete_rule=2)