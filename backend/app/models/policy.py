from mongoengine import Document, StringField, DictField
from . import AuditMixin, TimestampMixin

class Policy(Document, AuditMixin, TimestampMixin):
    meta = {'collection': 'policies'}  # Specifies the collection name

    name = StringField(required=True, unique=True)
    policy_json = DictField() 