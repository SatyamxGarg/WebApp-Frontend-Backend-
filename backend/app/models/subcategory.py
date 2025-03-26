from mongoengine import Document, StringField, ReferenceField
from . import TimestampMixin
from app.models.category import Category

class Subcategory(Document, TimestampMixin):
    meta = {'collection': 'subcategories'}  # Specifies the collection name
    
    subcategory_id = StringField(required=True, unique=True)
    subcategory_name = StringField(required=True, unique=True)
    subcategory_description = StringField()
    category = ReferenceField(Category, required=True, reverse_delete_rule=2)
