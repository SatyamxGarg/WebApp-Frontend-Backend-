from . import TimestampMixin
from mongoengine import Document, ReferenceField, ListField, FloatField, EnumField
from .user import User
from .product import Product
from enum import Enum

class OrderStatus(Enum):
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    
class PaymentStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

class Order(Document, TimestampMixin):
    meta = {'collection': 'order'}  # Specifies the collection name
    
    user = ReferenceField(User, required=True)
    product = ListField(ReferenceField(Product, required=True))
    total_price = FloatField(required=True)
    status = EnumField(OrderStatus, default=OrderStatus.PENDING)
    payment_status = EnumField(PaymentStatus, default=PaymentStatus.PENDING)