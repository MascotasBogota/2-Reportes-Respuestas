from mongoengine import Document, StringField, DateTimeField, PointField
from datetime import datetime

class Response(Document):
    meta = {
        'collection': 'responses',
        'indexes': [
            {'fields': ['report_id', 'created_at']},
            'resp_user_id'
        ]
    }
    report_id = StringField(required=True)
    resp_user_id = StringField(required=True)
    type = StringField(required=True, choices=['avistamiento', 'hallazgo'])
    comment = StringField(required=True)
    location = PointField()  # GeoJSON Point, opcional
    created_at = DateTimeField(default=datetime.now())