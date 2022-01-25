from asyncio import events
from typing import Dict, List
from pydantic import BaseModel, validator

class AddStudentSubscriptionSchema(BaseModel):
    student_id : str
    events : List[str]

    @validator("events")
    def validate_events(value):
        #TODO : add suitable doc string

        if len(value) == 0 :
            raise ValueError("events list should never be empty")

        event_names = ['new_internship','new_job']
        for val in value:
            if val.lower() not in event_names:
                raise ValueError(f'{val} is not a valid event')

        return value

