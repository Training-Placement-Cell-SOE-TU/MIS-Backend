from api.controllers.student import field_update_controller
from api.utils.exceptions import exceptions
from fastapi.responses import JSONResponse


async def update(request, user):
    try:

        if not user:
            return JSONResponse(status_code=403, content="JWT expired")

        response = await field_update_controller.update_personal_info(request, user)

        if response:
            return JSONResponse(status_code=200, content="personal info updated")

    except exceptions.UnauthorizedUser as e:
        return JSONResponse(status_code=403, content="user not authorized")

    except Exception as e:
        return JSONResponse(status_code=500, content="internal server error")
