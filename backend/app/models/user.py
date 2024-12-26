from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField, ListField, ReferenceField
from datetime import datetime
from app.utils.crypto import hash_password, verify_password
from . import TimestampMixin
from .policy import Policy
from .role import Role

class User(Document, TimestampMixin):
    meta = {'collection': 'users'}  # Specifies the collection name
    
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)  # Storing hashed passwords
    first_name = StringField(max_length=30)
    last_name = StringField(max_length=30)
    is_active = BooleanField(default=True)
    policies = ListField(ReferenceField(Policy))
    roles = ListField(ReferenceField(Role))
    
    def set_password(self, password):
        self.password_hash = hash_password(password) 
    
    def check_password(self, password):
        return verify_password(password, self.password_hash) 

