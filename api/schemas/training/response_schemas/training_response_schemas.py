from pydantic import BaseModel
from api.models.training.training import AttendanceForm
from typing import List

class GetTrainingSchema(BaseModel):
    training_id : str
    training_name : str
    training_desc : str
    training_venue : str
    attendance_form_links: List[AttendanceForm]
    training_start_date : str
    training_end_date : str
    training_time : str
    trainer_name : str
    trainer_desc: str