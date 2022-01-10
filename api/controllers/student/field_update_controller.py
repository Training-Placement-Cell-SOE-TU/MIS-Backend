from api.drivers.student import student_drivers
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions


async def update(
    request: student_request_schemas.StudentPersonalInfoSchema,
    user: str):
    """Updates student's personal info"""

    # Check if the user is updating it's own info 
    if user != request.student_id:
        raise exceptions.UnauthorizedUser(user, "update info")

    # Update personal info
    driver_response = await student_drivers.Student().update_general_info(request)

    if driver_response:
        return True

    
    
async def update_skill_info(request):
    pass

async def update_company_info(
    request: student_request_schemas.StudentCompanyInfoSchema):
    pass

async def update_company_letter_info(request):
    pass

async def update_certification_info(request):
    pass

async def update_scorecard_info(request):
    pass

async def update_internship_info(request):
    pass

async def update_social_info(request):
    pass
