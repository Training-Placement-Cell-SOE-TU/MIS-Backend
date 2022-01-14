import datetime
from os import environ

import jwt
import pydantic
from api.drivers.student import student_drivers
from api.middlewares import authentication_middleware
from api.models.student import student_model
from api.repository import student_repo
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )


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

    
    return student