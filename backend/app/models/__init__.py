from mongoengine import DateTimeField, EmailField
from mongoengine.base import BaseDocument
from datetime import datetime

class TimestampMixin(BaseDocument):
    meta = {
        'abstract': True,
        'indexes': [
            'updated_at'
        ]
    } 

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

class AuditMixin(BaseDocument):
    meta = {'abstract': True} 

    created_by = EmailField()
    updated_by = EmailField()
