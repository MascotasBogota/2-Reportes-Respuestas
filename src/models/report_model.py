from mongoengine import Document, StringField

class Report(Document):
    user_id = StringField(required=True)
    description = StringField()