from os import environ

import jwt
from api.middlewares import authentication_middleware
from api.repository import admin_repo, authentication_repo, student_repo
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


def construct_router():

    auth = APIRouter(
        tags="Authentication"
    )

    @auth.get("/refresh/token")
    async def refresh_token(request: Request):
        
        token = request.headers.get("Authorization", None)
    
        if token is not None:

            try:
                encoded_jwt = token.split(" ")[1]

                payload = jwt.decode(
                    encoded_jwt, 
                    environ.get("SECRET_KEY"), 
                    algorithms=[environ.get("JWT_ALGORITHM")]
                )
                
                response = authentication_repo.validate_refresh_token(payload)

                if not response:
                    return JSONResponse(
                        status_code = 500,
                        content = {
                            "message" : "internal server error"
                        }
                    )
            
                return JSONResponse(
                        status_code = 200,
                        content = {
                            "token" : response
                        }
                    )

            except jwt.ExpiredSignatureError:

                return JSONResponse(
                    status_code = 401,
                    content = {
                        "message" : "token expired"
                    }
                )


        return JSONResponse(
            status_code = 400,
            content = {
                "message": "Authorization Header not present"
            }
        )
    
        
        



    return auth
