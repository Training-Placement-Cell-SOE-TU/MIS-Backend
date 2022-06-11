from urllib.request import Request
from api.drivers.admin.admin_driver import Admin
from api.models import student
from api.models.admin.admin_model import AdminModel
from api.repository import admin_repo
from api.schemas.admin.admin_request_schema import admin_request_schemas
from fastapi import APIRouter
from passlib.hash import pbkdf2_sha256
from fastapi.responses import JSONResponse, RedirectResponse
import jwt
import datetime
from os import environ
from fastapi import APIRouter, Depends, HTTPException, Request, status


def construct_router():
    
    admin = APIRouter(
        tags=["Admin"]
    )

    @admin.post("/login")
    async def login(request: Request):
        """Handles Admin Login"""

        try:
            request = await request.json()

            admin = await AdminModel.find_one(
                AdminModel.email == request["email"]
            )

            if admin is None:
                return JSONResponse(
                    status_code=500,
                    content = {
                        "message": "admin doesn't exist"
                    }
                )

            if not pbkdf2_sha256.verify(request["password"], admin.password):
                return JSONResponse(
                    status_code=403,
                    content={
                        "message" : "Username or password incorrect"
                    }
                )

            jwt_payload = jwt.encode(
                {
                    "token" : admin.admin_id,
                    "role" : "student",
                    "exp": datetime.datetime.now(tz=datetime.timezone.utc) + 
                            datetime.timedelta(days = int(environ.get("JWT_EXP", 1)))
                },
                environ.get("SECRET_KEY"),
                algorithm=environ.get("JWT_ALGORITHM")
            )

            return JSONResponse(
                status_code=200,
                content = {
                    "token" : jwt_payload,
                    "username": admin.username
                }
            )

        except Exception as e:
            return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "internal server error"
                }
            )

    @admin.post("/add")
    async def add_admin(request: admin_request_schemas.AddAdminRequestSchema):

        response = await admin_repo.add_admin_handler(request.__dict__)
    
        return response


    return admin
