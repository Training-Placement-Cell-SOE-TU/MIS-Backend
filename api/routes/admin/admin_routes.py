from api.repository import admin_repo
from api.schemas.admin.admin_request_schema import admin_request_schemas
from fastapi import APIRouter


def construct_router():
    
    admin = APIRouter(
        tags=["Admin"]
    )

    @admin.post("/add")
    async def add_admin(request: admin_request_schemas.AddAdminRequestSchema):

        response = await admin_repo.add_admin_handler(request.__dict__)
    
        return response


    return admin
