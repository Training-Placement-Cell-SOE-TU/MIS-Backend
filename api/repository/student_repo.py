from api.controllers.student import field_update_controller
from api.utils.exceptions import exceptions
from fastapi.responses import JSONResponse


async def update_student(request, user):
    try:

        if not user:
            return JSONResponse(status_code=403, content={"message" : "token expired"})

        response = await field_update_controller.update(request, user)

        if response:
            return JSONResponse(status_code=200, content={"message" : "info updated"})

    except exceptions.UnauthorizedUser as e:
        return JSONResponse(status_code=403, content={"message" : "user not authorized"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message" : "internal server error"})
