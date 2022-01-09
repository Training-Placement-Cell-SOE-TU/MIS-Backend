
import datetime
from os import environ
import pprint
import jwt
import pydantic
from api.controllers.student import field_update_controller
from api.drivers.student import student_drivers
from api.middlewares import authentication_middleware
from api.models.student import student_model
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from api.utils.factory import student_factory
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )

    @student.get("/login", status_code=status.HTTP_200_OK)
    async def login(request: Request):
        request = await request.json()

        jwt_payload = jwt.encode(
            {
                "token" : request["user_id"],
                "exp": datetime.datetime.now(tz=datetime.timezone.utc) + 
                        datetime.timedelta(seconds=30)
            },
            environ.get("SECRET_KEY"),
            algorithm=environ.get("JWT_ALGORITHM")
        )

        return jwt_payload


    @student.get("/{roll_no}", status_code=status.HTTP_200_OK)
    async def get_student_by_roll(roll_no: str):
        return roll_no

    @student.get("/", status_code=status.HTTP_200_OK)
    async def get_student():
        pass


    @student.put("/update/personal", status_code=status.HTTP_200_OK)
    async def update_personal_info(
        request: student_request_schemas.StudentPersonalInfoSchema,
        authentication = Depends(authentication_middleware.is_authorized)):

        if not authentication:
            return JSONResponse(status_code=403, content="JWT expired")

        print(authentication)
        response = await field_update_controller.update_personal_info(request, authentication)

        if response:
            return JSONResponse(status_code=200, content="personal info updated")


    @student.post("/add")
    async def add_student(request: student_request_schemas.StudentPersonalInfoSchema):
        try:

            student = student_factory.StudentFactory.student(request)

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
