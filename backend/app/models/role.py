from mongoengine import Document, StringField, ListField, ReferenceField
from .policy import Policy
from . import AuditMixin, TimestampMixin

class Role(Document, AuditMixin, TimestampMixin):
    meta = {'collection': 'roles'}  # Specifies the collection name

    name = StringField(required=True, unique=True)
    policies = ListField(ReferenceField(Policy))  