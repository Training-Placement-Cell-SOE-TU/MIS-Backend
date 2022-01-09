from api.drivers.student import student_drivers
from api.schemas.student.request_schemas import student_request_schemas


async def update_personal_info(
    request: student_request_schemas.StudentPersonalInfoSchema,
    user):
    print("update personal info", user)
    return True
    
async def update_skill_info(request):
    pass

async def update_additional_info(request: 
    student_request_schemas.StudentAdditionalInfoSchema):
    pass

async def update_educational_info(request:
    student_request_schemas.StudentEducationalInfoSchema):
    pass

async def update_address_info(request:
    student_request_schemas.StudentAddressInfoSchema):
    pass

async def update_company_info(request:
    student_request_schemas.StudentCompanyInfoSchema):
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
