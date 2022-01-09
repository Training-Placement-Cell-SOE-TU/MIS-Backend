import datetime

from api.drivers.student import student_drivers
from api.schemas.student.request_schemas import student_request_schemas


class StudentFactory:
    """Factory method to select from different 
        students based on their batch.
    """

    @staticmethod
    def student(data: student_request_schemas.StudentPersonalInfoSchema):
        todays_date = datetime.date.today()

        if(data.batch < todays_date.year):
            return student_drivers.FormerStudent()
        
        return student_drivers.CurrentStudent()
