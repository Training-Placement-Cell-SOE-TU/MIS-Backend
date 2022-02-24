from pydantic import BaseModel, EmailStr


class AddTrainingSchema(BaseModel):
    training_name : str
    training_desc : str
    training_venue : str
    training_start_date : str
    training_end_date : str
    training_time : str
    trainer_name : str
    trainer_desc: str

    class Config:
        anystr_lower = True
    
class AddTrainingRegistration(BaseModel):
    training_id : str
    student_name : str
    student_rollno : str
    student_email : EmailStr 
    student_department : str
    enrolled_programme : str
    mobile : str
    yop_tu : int # validate yop_tu
    semester : str 

    class Config:
        anystr_lower = True