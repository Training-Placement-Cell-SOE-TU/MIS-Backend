from typing import Dict
from urllib.request import Request
from api.utils.exceptions import exceptions

from api.drivers.admin import admin_driver
from api.drivers.student import student_drivers
from api.utils.exceptions import exceptions
from api.utils.logger import Logger
from fastapi.responses import JSONResponse


def is_authenticated_and_authorized(request, authorization):

    # Check if user is authenticated and authorized
    if not authorization["flag"]:
        raise exceptions.AuthenticationError()
    
    if authorization["role"] != "admin":
        raise exceptions.UnauthorizedUser(authorization["role"])


async def operation_handler(request, authorization, fn):
    try:
        # Authorization check
        if type(request) == dict:
            is_authenticated_and_authorized(request, authorization)
        else:
            is_authenticated_and_authorized(request.__dict__, authorization)

        # Executes student instance method
        response = await fn(request)

        if response:
            return JSONResponse(status_code=200, 
            content={"message" : "admin operation executed"})
        
        return JSONResponse(status_code=200, 
            content={"message" : "admin operation cannot be executed"})


    except exceptions.AuthenticationError as e:

        return JSONResponse(status_code=403, 
            content={"message" : authorization["message"]})

    except exceptions.UnauthorizedUser as e:

        return JSONResponse(status_code=403, 
            content={"message" : "user not authorized"})

    except Exception as e:

        Logger.error(e, log_msg = "exception in operation_handler")
        
        return JSONResponse(status_code=500, 
        content={"message" : "internal server error"})


async def assign_otp(student_ids: Dict):
    is_failed = False
    for student_id in student_ids:
        response = await student_drivers.Student().add_token(student_id)

        if not response:
            is_failed = True

    
    return not is_failed


async def add_admin_handler(request):

    response = await admin_driver.Admin().add_admin(request)

    if response:
        return JSONResponse(
            status_code=200,
            content={
                "message" : "admin added successfully"
            }
        )
    
    return JSONResponse(
            status_code=404,
            content={
                "message" : "admin cannot be added"
            }
        )


async def get_admin_profile_handler(username, authorization):
    try:
        if not authorization["flag"]:
            raise exceptions.AuthenticationError()

        response = await admin_driver.Admin().get_admin_profile(username)

        if not response:
            return JSONResponse(
                status_code=404,
                content = {
                    "message": "admin not found"
                }
            )
    
        if authorization["token"] == response["admin_id"]:
           return JSONResponse(
                status_code=200,
                content={
                    "messsage": "auithorization successful"
                }
           )

    except exceptions.AuthenticationError as e:

        return JSONResponse(status_code=403, 
            content={"message" : authorization["message"]})