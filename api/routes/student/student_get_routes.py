from api.middlewares import authentication_middleware
from api.repository import student_repo
from api.schemas.student.response_schemas import student_response_schemas
from api.utils.logger import Logger
from fastapi import APIRouter, Depends, Request


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )

    @student.get('/{roll_no}')
    async def get_student_profile(
        roll_no: str,
        authorization = Depends(authentication_middleware.is_authenticated)):

        try:
            response = await (
                student_repo.get_student_profile_handler(roll_no, authorization)
            )

            return response
        
        except Exception as e:
            Logger.error(e, log_msg="exception in get_student_profile route")

    return student
