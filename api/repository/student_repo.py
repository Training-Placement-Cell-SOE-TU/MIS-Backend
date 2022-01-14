from api.drivers.student import student_drivers
from api.utils.exceptions import exceptions
from fastapi.responses import JSONResponse


def is_authenticated_and_authorized(request, authorization):

    # Check if user is authenticated and authorized
    if not authorization["flag"]:
        raise exceptions.AuthenticationError()
    
    if authorization["token"] != request["student_id"]:
        raise exceptions.UnauthorizedUser(
            authorization["token"], "add_to_array_of_dict")


async def update_handler(request, authorization, fn):
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
            content={"message" : "info updated"})


    except exceptions.AuthenticationError as e:

        return JSONResponse(status_code=403, 
            content={"message" : authorization["message"]})

    except exceptions.UnauthorizedUser as e:

        return JSONResponse(status_code=403, 
            content={"message" : "user not authorized"})

    except Exception as e:
        print(e)
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


async def add_to_array_of_dict(request, authorization, model_type):
    """Adds new object to field type list of objects in 
        authorized student's profile
    """
    
    student_id = request.student_id

    data = request.__dict__

    del data["student_id"]

    data = {
        "type" : model_type,
        "student_id" : student_id,
        "content" : data
    }

    response = await update_handler(
        data, 
        authorization, 
        student_drivers.Student().update_array_of_dict
    )

    return response


async def delete_to_array_of_dict(request, authorization):
    """Deletes new object to field type list of objects in 
        authorized student's profile
    """

    response = await update_handler(
        request, 
        authorization, 
        student_drivers.Student().delete_from_array_of_dict
    )

    return response

