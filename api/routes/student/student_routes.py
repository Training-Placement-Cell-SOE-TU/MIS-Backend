
import pydantic
from api.drivers.student import student_drivers
from api.models.student import student_model
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from api.utils.factory import student_factory
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )


    @student.get("/{roll_no}", status_code=status.HTTP_200_OK)
    async def get_student_by_roll(roll_no: str):
        return roll_no

    @student.get("/", status_code=status.HTTP_200_OK)
    async def get_student():
        pass


    @student.post("/add")
    async def add_student(request: student_request_schemas.RegisterStudent):
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
