import jwt
from api.middlewares import authentication_middleware
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from api.repository import admin_repo, student_repo

def construct_router():

    auth = APIRouter(
        tags="Authentication"
    )

    @auth.get("/refresh/token")
    async def refresh_token(
        authorization = Depends(authentication_middleware.is_authenticated)):

        if not authorization["flag"]:
            return JSONResponse(
                status_code=403,
                content={
                    "message" : authorization["message"]
                }
            )
        
        # roles = {
        #     "admin" : 
        # }
    
        
        



    return auth
