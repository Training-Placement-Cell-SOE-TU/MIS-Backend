from typing import Dict
from uuid import uuid4

from api.models.student.skill_model import SkillsModel
from api.models.student.student_model import *
from api.schemas.student.request_schemas import student_request_schemas
from api.utils import otp_generator
from api.utils.exceptions import exceptions
from api.utils.logger import Logger
from api.utils.model_mappings import model_mappings
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
from pymongo.errors import DuplicateKeyError


class Student:
    """
        Student database driver.
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

            if student is None:
                return False

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

            if student is None:
                return False

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

            if student is None:
                return False

            field_type = info["model_type"]

            # Gets current data of input field to delete 
            field_data = getattr(student, field_type)

            # Deletes the specified data
            for i in field_data:
                if i.uid == info["uid"]:
                    field_data.remove(i)
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


    async def update_array_of_str(self, info: Dict):
        #TODO : add a suitable doc string
        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == info["student_id"]
            )
            if student is None:
                return False
            del info["student_id"]


            key , value = list(info.items())[0]
            field_name = getattr(student, key)
            field_name.extend(value)
            setattr(student, key, field_name)
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


    async def delete_from_array_of_str(self, info: Dict):
        #TODO: add a suitable doc string
        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == info["student_id"]
            )

            if student is None:
                return False

            del info["student_id"]


            key , value = list(info.items())[0]

            field_name = getattr(student, key)
            
            counter = 0

            for val in value:
                if val in field_name:
                    field_name.remove(val)
                else:
                    counter += 1
            
            if counter == len(value):
                return False

            setattr(student, key, field_name)
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


    async def update_password(self, info: Dict):
        #TODO : add a suitable doc string
        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == info["student_id"]
            )
            if student is None:
                return False

            del info["student_id"]


            student.password = pbkdf2_sha256.hash(str(info["password"]))
            student.student_id = str(uuid4())
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


    async def add_token(self, info: str):
        #TODO : add a suitable doc string
        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == info
            )

            if student is None:
                return False

            student.token = str(otp_generator.otp_generator(6))
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


    async def verify_student(self, info: Dict):
        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == info["student_id"]
            )

            if student is None:
                return False

            if student.token == info["otp"]:
                student.is_account_active = True
                student.token = ""
            else:
                return "wrong_otp"
            


            db_response = await StudentModel.save(student)

            if db_response:
                return True

            return False

        except DuplicateKeyError as e:
            #TODO: log to logger
            print(f"{e} dupkey err : student driver")
            raise exceptions.DuplicateStudent()

        except Exception as e:
            Logger.error(e, log_msg="exception in verify_student")
            raise exceptions.UnexpectedError()


    async def ban_student(self, student_id: str):
        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == student_id
            )

            if student is None:
                return False

            if not student.is_account_active:
                print("alerady_banned")
                return "already_banned"

            student.is_account_active = False

            db_response = await StudentModel.save(student)

            if db_response:
                    return True

            return False

        except DuplicateKeyError as e:
            #TODO: log to logger
            print(f"{e} dupkey err : student driver")
            raise exceptions.DuplicateStudent()

        except Exception as e:
            #TODO: log to logger
            print(f"{e} excep err : student driver")
            raise exceptions.UnexpectedError()


    async def delete_student(self, student_id: str):
        try:
            student = await StudentModel.find_one(
                StudentModel.student_id == student_id
            )

            if student is None:
                return False

            await student.delete()

            return True

        except DuplicateKeyError as e:
            #TODO: log to logger
            print(f"{e} dupkey err : student driver")
            raise exceptions.DuplicateStudent()

        except Exception as e:
            #TODO: log to logger
            print(f"{e} excep err : student driver")
            raise exceptions.UnexpectedError()


    async def update_array_of_refs(self, info: Dict):
        #TODO: add suitable doc string and exception handling

        student = await StudentModel.find_one(
            StudentModel.student_id == info["student_id"]
        )

        if student is None:
            return False
        
        del info["student_id"]

        key, values = list(info.items())[0]

        # Get respective field  value
        field_value = getattr(student, key)

        counter = 0

        for value in values:

            # If value is not already present then execute
            value = ObjectId(value)
            if value not in field_value:
                field_value.append(value)
            else:
                counter += 1
        
        if counter == len(values):
            return False


        # Setting updated array to the key
        setattr(student, key, field_value)

        # Commiting changes in db
        db_response = await StudentModel.save(student)

        if db_response:
            
            return True

        return False


    async def get_student_profile(self, roll_no: str):
        #TODO: add suitable doc string and exception handling
        student = await StudentModel.find_one(
            StudentModel.roll_no == roll_no
        )

        if student is None:
            return False
        
        if len(student.skills) == 0:
            return student.__dict__

        skill_names = []

        for val in student.skills:
            skill = await SkillsModel.find_one(
                {"_id" : val}
            )

            if skill is not None:
                skill_names.append(skill.skill_name)

        student.skills = skill_names        

        return student.__dict__

        
    async def set_refresh_token(self, user_id: str):
        student = await StudentModel.find_one(
            StudentModel.student_id == user_id
        )

        if student is None:
            return False

        token = str(uuid4())

        student.refresh_token = token

        # Commiting changes in db
        db_response = await StudentModel.save(student)

        if db_response:
            
            return token

        return False

    async def check_refresh_token(self, info):
        student = await StudentModel.find_one(
            StudentModel.student_id == info["user_id"]
        )

        if student is None:
            return False
        
        if student.refresh_token == info["token"]:
            return True
        

        return False