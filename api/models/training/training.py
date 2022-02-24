from uuid import uuid4
from pydantic import BaseModel, EmailStr
from beanie import Document
from typing import Optional, List
from api.models.general_use_models import PydanticObjectId



class AttendanceForm(BaseModel):
    shift : str
    form_link : str

class TrainingRegistrations(Document):
    training_id : str
    student_id : str = str(uuid4())
    student_name : str
    student_rollno : str
    student_email : EmailStr #gmail only
    student_department : str
    enrolled_programme : str
    mobile : str
    yop_tu : int
    semester : str #(I - X)

    class Config:
        anystr_lower = True

    class Collection:
        name = "training_registrations"


class TrainingModel(Document):
    training_id : str = str(uuid4())
    training_name : str
    training_desc : str
    training_venue : str
    attendance_form_links : List[AttendanceForm] = []

    # Duration can be derived from start and end date
    training_start_date : str
    training_end_date : str
    training_time : str

    # Trainer details (Can be shifted to separate collection later)
    trainer_avatar: str = "https://i.ibb.co/pR6C9MZ/deafult-avatar.jpg"
    trainer_name : str
    trainer_desc: str

    class Collection:
        name = "training"

