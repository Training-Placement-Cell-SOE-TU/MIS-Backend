from api.middlewares import authentication_middleware
from api.repository import admin_repo
from api.schemas.student.response_schemas import student_response_schemas
from api.utils.logger import Logger
from fastapi import APIRouter, Depends, Request


def construct_router():
    
    admin = APIRouter(
        tags=["Admin"]
    )

    @admin.get('/{username}/admin-console/{nav}')
    async def get_admin_console(
        username: str,
        nav: str,
        authorization = Depends(authentication_middleware.is_authenticated)):

        try:
            print(username)
            response = await (
                admin_repo.get_admin_profile_handler(username, authorization)
            )
            print(response)

            return response

        except Exception as e:
            Logger.error(e, log_msg="exception in get_admin_profile route")


    return admin