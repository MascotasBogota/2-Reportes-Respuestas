from mongoengine import Document, StringField, PointField, ListField, DateTimeField
from datetime import datetime

class Report(Document):
    user_id = StringField(required=True)
    type = StringField(required=True, choices=["perro", "gato", "otro"])
    description = StringField(required=True)
    location = PointField(required=True)
    images = ListField(StringField())
    status = StringField(default="open", choices=["open", "closed"])
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    closed_at = DateTimeField()
