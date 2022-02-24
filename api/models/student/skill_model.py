from uuid import uuid4
from pydantic import BaseModel
from beanie import Document
from typing import Optional, List

class SkillsModel(Document):
    skill_id : str = str(uuid4())
    skill_name : str
    tags : Optional[List[str]] = []

    class Config:
        anystr_lower = True
        

    class Collection:
        name = "skills"

