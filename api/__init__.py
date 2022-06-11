import asyncio
from datetime import datetime
from os import environ, path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import errors

from api.config.database import database
from api.routes.admin import (admin_get_routes, admin_routes, admin_student_routes,
                              admin_training_routes)
from api.routes.student import (student_add_routes, student_delete_routes,
                                student_general_routes, student_get_routes,
                                student_update_routes)

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

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
            #TODO: log error and continuous retry
            print("DB Timeout")
            pass

        except errors.DuplicateKeyError as e:
            #TODO: Critical error, notify to admin and dev
            print("DUPLICATE")

        except Exception as e:
            #TODO: Notify admin

            print("EXCEPTION", e)


    # Triggers functions on shutdown
    @app.on_event("shutdown")
    async def shutdown_event():
        print("SHUTDOWN")

    @app.get("/")
    async def index():
        return {"message" : "running"}

    # Register all the routers
    app.include_router(
        student_general_routes.construct_router(),
        prefix = "/student"
    )

    app.include_router(
        student_get_routes.construct_router(),
        prefix = "/student"
    )

    app.include_router(
        student_add_routes.construct_router(),
        prefix = "/student"
    )

    app.include_router(
        student_update_routes.construct_router(),
        prefix = "/student"
    )

    app.include_router(
        student_delete_routes.construct_router(),
        prefix = "/student"
    )

    app.include_router(
        admin_routes.construct_router(),
        prefix = "/admin"
    )

    app.include_router(
        admin_get_routes.construct_router(),
        prefix="/admin"
    )

    app.include_router(
        admin_student_routes.construct_router(),
        prefix = "/admin"
    )

    app.include_router(
        admin_training_routes.construct_router(),
        prefix = "/training"
    )

    
    return app
