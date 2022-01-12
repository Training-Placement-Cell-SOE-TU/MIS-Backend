import datetime

from beanie import Document
from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class NotificationModel(Document):
    """Stores all the notifications of different users."""

    user_id: PydanticObjectId
    notification_header: str
    notification_body: str
    datetime = datetime.datetime.now()
