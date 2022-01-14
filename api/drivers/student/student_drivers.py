from abc import ABC, abstractmethod
from typing import Dict, final

import pydantic
from api.models.student.student_model import *
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from api.utils.model_mappings import model_mappings
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


    async def update_general_info(self, info):

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


    async def update_array_of_dict(self, info):

        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == info["student_id"]
            )
            
            info_type = info["type"]

            # Gets model corresponding to field type
            model = model_mappings[info_type]

            # Initiates model with incoming data for auto-generating of index fields
            data_to_append = model(**info["content"])

            data_to_append = data_to_append.__dict__

            # Gets current data of field to update
            field_data = getattr(student, info_type)

            # Appends incoming data to fetched field data
            field_data.append(data_to_append)

            # Updates class with appended field data
            setattr(student, info_type, field_data)

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

    

    async def delete_from_array_of_dict(self, info: dict):
        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == info["student_id"]
            )
            
            field_type = info["model_type"]

            # Gets current data of input field to delete 
            field_data = getattr(student, field_type)

            # Deletes the specified data
            for i in len(field_data):
                if field_data[i]["uid"] == info["uid"]:
                    del field_data[i]
                    break

            # Updates class with appended field data
            setattr(student, field_type, field_data)

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
    def delete_student():
        pass

