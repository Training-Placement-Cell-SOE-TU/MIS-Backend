from datetime import datetime
from typing import List
from uuid import uuid4

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

class CompanyPostModel(Document):
    """Company Post Model"""

    company_id: List[PydanticObjectId] = []
    post_id: str = str(uuid4())
    posted_on: datetime = datetime.now()
    role_offered: str
    role_description: str
    required_skills: List[str] = []


    class Settings:
        validate_on_save = True

    class Collection:
        name = "company_posts"
