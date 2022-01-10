from abc import ABC, abstractmethod
from typing import Dict, final

import pydantic
from api.models.student.student_model import StudentModel
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from passlib.hash import pbkdf2_sha256
from pymongo.errors import DuplicateKeyError


class Student:
    """Student database driver.
        Responsible for various student related
        tasks.
    """

    async def add_student(self, 
        student_details: student_request_schemas.RegisterStudentSchema):

        """Adds new student to the database"""

        try:

            student = StudentModel(**student_details.__dict__)
            
            student.password = pbkdf2_sha256.hash(student.password)

            db_response = await StudentModel.save(student)
            
            return True

        except DuplicateKeyError as e:
            #TODO: log to logger
            print(f"{e} dupkey err : student driver")
            raise exceptions.DuplicateStudent()

        except Exception as e:
            #TODO: log to logger
            print(f"{e} excep err : student driver")
            raise exceptions.UnexpectedError()


    async def update_general_info(self, 
        info: pydantic.BaseModel):

        """Updates students data for general field"""

        try:

            student = await StudentModel.find_one(
                StudentModel.student_id == info.student_id
            )

            info = info.__dict__

            del info["student_id"]

            for key, value in info.items():
                setattr(student, key, value)

            db_response = await StudentModel.save(student)
            
            return True

        except DuplicateKeyError as e:
            #TODO: log to logger
            print(f"{e} dupkey err : student driver")
            raise exceptions.DuplicateStudent()

        except Exception as e:
            #TODO: log to logger
            print(f"{e} excep err : student driver")
            raise exceptions.UnexpectedError()


    @abstractmethod
    def get_student():
        pass

    @abstractmethod
    def ban_student():
        pass

    @abstractmethod
    def delete_student():
        pass

