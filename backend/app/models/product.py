from . import TimestampMixin
from mongoengine import Document, StringField, IntField, FloatField

class Product(Document, TimestampMixin):
    meta = {'collection': 'products'}  # Specifies the collection name
    
    product_name = StringField(required=True)
    product_id = StringField(required=True, Unique=True)
    product_description = StringField()
    product_price = FloatField(required=True)
    product_stock = IntField(required=True)