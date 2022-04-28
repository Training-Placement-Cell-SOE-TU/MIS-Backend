import datetime
from pydantic import BaseModel, EmailStr , validator


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
    yop_tu : int
    semester : str 

    class Config:
        anystr_lower = True

    # validate year of passing
    @validator('yop_tu' , always=True)
    def validate_yop(cls , value):
        """Year Of Passing should not be greater than current year + 4"""
        
        todays_date = datetime.date.today()

        if((todays_date.year + 4) < value):
            raise ValueError("Year Of Passing greater than current year + 4 is not allowed")
        
        return value

    @validator('yop_tu', always=True)
    def check_batch_lt_1994(cls, value):
        """Year Of Passing should not be less than year of establishment"""

        if(value < 1994):
            raise ValueError("Tezpur University did not exist before 1994")
        
        return value