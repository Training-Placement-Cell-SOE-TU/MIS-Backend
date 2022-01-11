from api.drivers.student import student_drivers
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions


async def update(
        request: student_request_schemas.StudentPersonalInfoSchema,
        authorization
    ):
    """Updates student's info"""

    # Check if the user is updating it's own info 
    if authorization["token"] != request.student_id:
        raise exceptions.UnauthorizedUser(authorization["token"], "update info")

    # Update personal info
    driver_response = await student_drivers.Student().update_general_info(request)

    if driver_response:
        return True

    
    
async def update_skill_info(request):
    pass


