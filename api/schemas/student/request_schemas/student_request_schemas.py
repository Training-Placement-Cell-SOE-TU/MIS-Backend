from pydantic import BaseModel

class GetStudent(BaseModel):
    roll_no: str