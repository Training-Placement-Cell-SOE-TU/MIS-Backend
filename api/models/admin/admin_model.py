from typing import List
from uuid import uuid4

from beanie import Document, Indexed


class AdminModel(Document):
    admin_id: Indexed(str, unique = True) = str(uuid4())
    refresh_token: str = ''
    username: str
    email: Indexed(str, unique = True)
    password: str 
    scopes: List[str] = []

    class Config:
        anystr_lower = True

    class Collection:
        name = "admin"
