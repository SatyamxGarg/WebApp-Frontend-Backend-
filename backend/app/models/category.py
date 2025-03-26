from . import TimestampMixin
from mongoengine import Document, StringField

class Category(Document, TimestampMixin):
    meta = {'collection': 'categories'}  # Specifies the collection name
    
    category_id = StringField(required=True, unique=True)
    category_name = StringField(required=True, unique=True)
    category_description = StringField(max_length=500)
