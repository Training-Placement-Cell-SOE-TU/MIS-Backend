
import datetime
import pprint
from os import environ

import jwt
import pydantic
from api.controllers.student import field_update_controller
from api.drivers.student import student_drivers
from api.middlewares import authentication_middleware
from api.models.student import student_model
from api.repository import student_repo
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from api.utils.factory import student_factory
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )

    @student.post("/login", status_code=status.HTTP_200_OK)
    async def login(request: Request):
        try:
            request = await request.json()

            jwt_payload = jwt.encode(
                {
                    "token" : request["user_id"],
                    "exp": datetime.datetime.now(tz=datetime.timezone.utc) + 
                            datetime.timedelta(days = int(environ.get("JWT_EXP", 1)))
                },
                environ.get("SECRET_KEY"),
                algorithm=environ.get("JWT_ALGORITHM")
            )

            return JSONResponse(content={"token" : jwt_payload})

        except Exception as e:
            return JSONResponse(status_code=500, content = {"message" : "internal server error"})


    @student.get("/{roll_no}", status_code=status.HTTP_200_OK)
    async def get_student_by_roll(roll_no: str):
        return roll_no

    @student.get("/", status_code=status.HTTP_200_OK)
    async def get_student():
        pass


    @student.put("/update/personal", status_code=status.HTTP_200_OK)
    async def update_personal_info(
        request: student_request_schemas.StudentPersonalInfoSchema,
        authorization = Depends(authentication_middleware.is_authenticated)):

        """Student personal info update route"""

        response = await student_repo.update_student(
            request, authorization
        )
        return response



    @student.put("/update/additional", status_code=status.HTTP_200_OK)
    async def update_additional_info(
        request: student_request_schemas.StudentAdditionalInfoSchema,
        authorization = Depends(authentication_middleware.is_authenticated)):

        """Student additional info update route"""

        response = await student_repo.update_student(
            request, authorization
        )
        return response


    @student.put("/update/educational", status_code=status.HTTP_200_OK)
    async def update_educational_info(
        request: student_request_schemas.StudentEducationalInfoSchema,
        authorization = Depends(authentication_middleware.is_authenticated)):

        """Student educational info update route"""

        response = await student_repo.update_student(
            request, authorization
        )
        return response

    
    @student.put("/update/address", status_code=status.HTTP_200_OK)
    async def update_address_info(
            request: student_request_schemas.StudentAddressInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):

        """Student address info update route"""

        response = await student_repo.update_student(
            request, authorization
        )
        return response



    @student.post("/add/letters", status_code=status.HTTP_200_OK)
    async def add_company_letters(
            request: student_request_schemas.StudentCompanyLetterInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles company letter addition to student's profile"""

        student_id = request.student_id

        data = request.__dict__

        del data["student_id"]

        data = {
            "type" : "company_letters",
            "student_id" : student_id,
            "content" : data
        }

        response = await student_repo.add_to_array_of_dict(
            data, authorization
        )
        return response

    @student.post("/add/social", status_code=status.HTTP_200_OK)
    async def add_company_letters(
            request: student_request_schemas.StudentSocialInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles social profile addition to student's profile"""

        student_id = request.student_id

        data = request.__dict__

        del data["student_id"]

        data = {
            "type" : "social_links",
            "student_id" : student_id,
            "content" : data
        }

        response = await student_repo.add_to_array_of_dict(
            data, authorization
        )
        return response


    @student.post("/add")
    async def add_student(request: student_request_schemas.RegisterStudentSchema):
        try:

            student = student_drivers.Student()

            response = await student.add_student(request)
            
            message = "student created"

            return JSONResponse(
                status_code=status.HTTP_201_CREATED, 
                content=message
            )

        except exceptions.UnexpectedError as e:
            #TODO: log to logger

            return JSONResponse(
                status_code=500,
                content="unexpected error occured"
            )

        except exceptions.DuplicateStudent as e:
            #TODO: log to logger

            return JSONResponse(
                status_code=409,
                content="student already exists"
            )

    


    return student
