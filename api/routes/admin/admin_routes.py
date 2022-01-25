from fastapi import  APIRouter, Depends, requests, status, HTTPException
from api.middlewares import authentication_middleware
from api.schemas.admin.admin_request_schema import admin_request_schemas
from api.drivers.student import student_drivers
from api.utils.exceptions import exceptions 
from fastapi.responses import JSONResponse

def construct_router():

    admin = APIRouter(
        tags=["Admin"]
    )

    @admin.post('/notify/student')
    async def notify_by_batch():
        pass

    @admin.post('/add/student/subscription')
    async def add_student_subscription(
        request : admin_request_schemas.AddStudentSubscriptionSchema
    ):
        try:
            response = await student_drivers.Student().update_array_of_str(request.__dict__)
            return JSONResponse(
                status_code=200,
                content={"message" : "info updated"}
            )
        
        except exceptions.DuplicateStudent: 
            return JSONResponse(
                status_code=409,
                content={"message" : "info cannot be updated"}
            )

        except exceptions.UnexpectedError:
            return JSONResponse(
                status_code=500,
                content={"message" : "internal server error"}
            )

        


    @admin.post('/remove/student/subscription')
    async def remove_student_subscription():
        pass

    @admin.post('/verify/student')
    async def verify_student():
        pass

    return admin
