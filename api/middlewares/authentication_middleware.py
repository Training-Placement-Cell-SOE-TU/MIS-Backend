from os import environ

import jwt
from fastapi import Request


def is_authorized(request: Request):

    token = request.headers.get("Authorization", None)
    
    if token is not None:

        try:
            encoded_jwt = token.split(" ")[1]

            payload = jwt.decode(
                        encoded_jwt, 
                        environ.get("SECRET_KEY"), 
                        algorithms=[environ.get("JWT_ALGORITHM")]
                    )
            
            return payload["token"]
        
        except jwt.ExpiredSignatureError:

            return False
