import asyncio
from os import path, environ

from dotenv import load_dotenv
from fastapi import FastAPI

from api.config.database import database
from api.routes.admin import admin_routes
from api.routes.student import student_routes



BASE_DIR = path.abspath(path.dirname(__file__))



def create_app():

    description = """
        School of Engineering, Tezpur University

        Backend API for Training & Placement Cell Portal

    """

    # Initialize fastapi app
    app = FastAPI(
        title = "MIS Backend API",
        description = description
    )


    # Triggers functions on startup
    @app.on_event("startup")
    async def startup_event():
        try:

            # Loading environment variables from environment file
            load_dotenv(path.join(BASE_DIR, '.env'))
            
            # Connect with database
            await asyncio.wait_for(database(), timeout=60.0)

        except asyncio.TimeoutError as e:
            #TODO: log error
            print("DB Timeout")
            pass



    # Register all the routers
    app.include_router(
        student_routes.construct_router(),
        prefix = "/student"
    )

    app.include_router(
        admin_routes.construct_router(),
        prefix = "/admin"
    )

    
    return app
