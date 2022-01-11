from api.drivers.student import student_drivers
from api.utils.exceptions import exceptions
from fastapi.responses import JSONResponse


def is_authenticated_and_authorized(authorization):

    # Check if user is authenticated and authorized
    if not authorization["flag"]:
        raise exceptions.AuthenticationError()
    
    if authorization["token"] != request.student_id:
        raise exceptions.UnauthorizedUser(
            authorization["token"], "add_to_array_of_dict")


async def update_handler(da, authorization, fn):
    try:
        # Authorization check
        is_authenticated_and_authorized(authorization)

        # Create student object
        student = student_drivers.Student()

        # Executes student instance method
        response = await fn(da)
        print(f"{response}: response update handler")

        if response:
            return JSONResponse(status_code=200, 
            content={"message" : "info updated"})


    except exceptions.AuthenticationError as e:

        return JSONResponse(status_code=403, 
            content={"message" : authorization["message"]})

    except exceptions.UnauthorizedUser as e:

        return JSONResponse(status_code=403, 
            content={"message" : "user not authorized"})

    except Exception as e:

        return JSONResponse(status_code=500, 
        content={"message" : "internal server error"})


async def update_student(request, authorization):
    """Updates student's general info"""

    response = await update_handler(
        request, 
        authorization, 
        student_drivers.Student().update_general_info
    )

    return response



async def add_to_array_of_dict(d, authorization):
    """Adds new company letter to authorized student's profile"""
    print(d)
    try:
        # Authorization check
        is_authenticated_and_authorized(authorization)

        # Create student object
        student = student_drivers.Student()

        # Executes student instance method
        response = await student.update_array_of_dict(d)

        if response:
            return JSONResponse(status_code=200, 
            content={"message" : "info updated"})


    except exceptions.AuthenticationError as e:

        return JSONResponse(status_code=403, 
            content={"message" : authorization["message"]})

    except exceptions.UnauthorizedUser as e:

        return JSONResponse(status_code=403, 
            content={"message" : "user not authorized"})

    except Exception as e:
        print(f"{e}")
        return JSONResponse(status_code=500, 
        content={"message" : "internal server error"})
