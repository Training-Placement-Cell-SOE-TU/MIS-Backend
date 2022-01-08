from abc import ABC, abstractmethod
from typing import Dict, final

from api.models.student import student_model
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from passlib.hash import pbkdf2_sha256
from pymongo.errors import DuplicateKeyError


class Student(ABC):
    """Student database driver.
        Responsible for various student related
        tasks.
    """

    async def add_student(
        self, 
        student_details: student_request_schemas.RegisterStudent):

        """Adds new student to the database"""

        try:

            student = student_model.StudentModel(**student_details.__dict__)
            
            student.password = pbkdf2_sha256.hash(student.password)

            db_response = await student_model.StudentModel.save(student)
            
            return True

        except DuplicateKeyError as e:
            #TODO: log to logger
            print(f"{e} dupkey err : student driver")
            raise exceptions.DuplicateStudent()
        
        except ValueError as e:
            #TODO: log to logger
            print(f"{e} val err : student driver")
            raise exceptions.UnexpectedError()

        except Exception as e:
            #TODO: log to logger
            print(f"{e} excep err : student driver")
            raise exceptions.UnexpectedError()


    @abstractmethod
    def update_student():
        pass

    @abstractmethod
    def get_student():
        pass

    @abstractmethod
    def ban_student():
        pass

    @abstractmethod
    def delete_student():
        pass


@final
class CurrentStudent(Student):
    """Current student database driver.
        Performes all tasks related to current student
    """


    def update_student(student_id: str, fields_to_update: Dict[str, str]):
        pass

    def get_student(search_fields):
        pass

    def ban_student(student_rollno: str):
        pass

    def delete_student(student_rollno: str):
        pass


@final
class FormerStudent(Student):
    """Former student database driver.
        Performes all tasks related to current student
    """


    def update_student(student_id: str, fields_to_update: dict):
        pass

    def get_student(search_fields: dict):
        pass

    def ban_student(student_rollno: str):
        pass

    def delete_student(student_rollno: str):
        pass
