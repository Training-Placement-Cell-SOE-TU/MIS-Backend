from typing import List

from api.drivers.student import skills_model_driver
from fastapi.responses import JSONResponse
from api.utils.logger import Logger

async def add_skills_handler(skills: List):

    try:

        failed_skills = []

        for skill in skills:
            response = await skills_model_driver.Skills().add_skills(skill)

            if not response:
                failed_skills.append(skill["skill_name"])
            
        if len(failed_skills) == 0:
            return JSONResponse(
                status_code = 200,
                content = {
                    "message" : "skills added successfully"
                }
            )

        return JSONResponse(
            status_code = 404,
            content = {
                "message" : "some skills cannot be added",
                "failed_skills" : failed_skills 
            }
        )

    except Exception as e:
        
        Logger.error(e, log_msg="exception at add_skills_handler")

        return JSONResponse(
            status_code = 500,
            content = {
                "message" : "internal server error"
            }
        )