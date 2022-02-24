import datetime
from os import environ

import jwt
from api.drivers.student import student_drivers


async def validate_refresh_token(payload):
    user_array = {
        "admin" : "", # TODO: insert actual function
        "student": student_drivers.Student().check_refresh_token,
        "company": ""
    }

    info = {
        "user_id" : payload["user_id"],
        "token" : payload["refresh_token"]
    }

    role = payload["role"]

    fn = user_array[role]

    response = fn(info)

    if not response:
        return False
    
    jwt_payload = jwt.encode(
        {
            "token" : payload["user_id"],
            "role" : "student",
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + 
                    datetime.timedelta(days = int(environ.get("JWT_EXP", 1)))
        },
        environ.get("SECRET_KEY"),
        algorithm=environ.get("JWT_ALGORITHM")
    )

    return jwt_payload
