from typing import Dict
from urllib.request import Request
from api.drivers.student import student_drivers



async def assign_otp(student_ids: Dict):
    is_failed = False
    for student_id in student_ids:
        response = await student_drivers.Student().add_token(student_id)

        if not response:
            is_failed = True

    
    return not is_failed


