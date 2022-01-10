
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
        user = Depends(authentication_middleware.is_authorized)):

        """Student personal info update route"""

        response = await student_repo.update_student(request, user)
        return response



    @student.put("/update/additional", status_code=status.HTTP_200_OK)
    async def update_additional_info(
        request: student_request_schemas.StudentAdditionalInfoSchema,
        user = Depends(authentication_middleware.is_authorized)):

        """Student additional info update route"""

        response = await student_repo.update_student(request, user)
        return response


    @student.put("/update/educational", status_code=status.HTTP_200_OK)
    async def update_educational_info(
        request: student_request_schemas.StudentEducationalInfoSchema,
        user = Depends(authentication_middleware.is_authorized)):

        """Student educational info update route"""

        response = await student_repo.update_student(request, user)
        return response

    
    @student.put("/update/address", status_code=status.HTTP_200_OK)
    async def update_address_info(
        request: student_request_schemas.StudentAddressInfoSchema,
        user = Depends(authentication_middleware.is_authorized)):

        """Student address info update route"""

        response = await student_repo.update_student(request, user)
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

    @student.post("/ban", status_code=status.HTTP_200_OK)
    async def ban_student():
        pass


    @student.delete("/delete", status_code=status.HTTP_200_OK)
    async def delete_student():
        pass


    return student
