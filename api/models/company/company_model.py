from datetime import datetime
from typing import List

from beanie import Document, Indexed
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


class CompanyModel(Document):
    """Company Model"""

    company_name: str
    company_id: str
    creation_datetime: datetime = datetime.now()
    company_email: Indexed(str, unique=True) #TODO: Validators --> email validation
    password: str #TODO: Validators --> password strength checker
    posts: List[PydanticObjectId] = []

    class Settings:
        validate_on_save = True

    class Collection:
        name = "company"
