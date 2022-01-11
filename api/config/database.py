import asyncio
from os import environ

import motor
from api.models.company.company_model import CompanyModel
from api.models.company.company_post_model import CompanyPostModel
from api.models.student.student_model import StudentModel
from beanie import init_beanie


async def database():

    # Create Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(
        environ.get("DEV_DB_URI"), tls=True, tlsAllowInvalidCertificates=True
    )

    await init_beanie(
        database = client.tnpcell,
        document_models = [
            CompanyModel,
            CompanyPostModel,
            StudentModel
        ]
    )
   