"""
    Authentication system is not integrated yet.
    Remove this when it's integrated
"""


import json as j
from os import path

from api.models.training.training import (AttendanceForm, TrainingModel,
                                          TrainingRegistrations)
from api.schemas.training.request_schemas import training_request_schemas
from api.schemas.training.response_schemas import training_response_schemas
from api.utils.logger import Logger
from bson.objectid import ObjectId
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import JSONResponse
from api.utils.send_email import send_email

def construct_router():

    training = APIRouter(
        tags=["Training"]
    )

    @training.get("/all")
    async def get_all_trainings(request: Request):
        try:

            trainings = await TrainingModel.find_all().to_list()
            
            result = []
            for tr in trainings:
                result.append(
                    j.loads(
                        j.dumps(
                            training_response_schemas
                            .GetTrainingSchema(**tr.__dict__).__dict__, 
                            default=lambda o: o.__dict__
                        )
                    )
                )

            return JSONResponse(
                status_code = 200,
                content = {
                    "result" : result
                }
            )
        except Exception as e:
            Logger.error(e)

            return JSONResponse(
                status_code = 500,
                content = {
                    "message" : "internal server error"
                }
            )


    @training.post("/add")
    async def add_new_training(request: training_request_schemas.AddTrainingSchema):
        try:

            trainings = TrainingModel(**request.__dict__)

            db_response = await TrainingModel.save(trainings)

            if db_response:
                return JSONResponse(    
                    status_code = 200,
                    content = {
                        "message" : "training added successfully"
                    }
                )
            
            return JSONResponse(
                    status_code = 500,
                    content = {
                        "message" : "training cannot be added"
                    }
                )
        except Exception as e:
            Logger.error(e)


    @training.post("/add/attendance")
    async def add_attendance_form_link(request: Request):
        try:
            request = await request.json()

            # Find if training exists
            trainings = await TrainingModel.find_one(
                TrainingModel.training_id == request["training_id"]
            )

            if trainings is None:
                return JSONResponse(
                    status_code = 404,
                    content = {
                        "message" : "invalid training"
                    }
                )
            
            del request["training_id"]

            attendance_link = AttendanceForm(**request)
            trainings.attendance_form_links.append(attendance_link)

            db_response = await trainings.save()

            if db_response:
                return JSONResponse(
                    status_code = 200,
                    content = {
                        "message" : "attendance link added"
                    }
                )
            
            return JSONResponse(
                status_code = 500,
                content = {
                    "message" : "attendance link cannot be added"
                }
            )

        except Exception as e:
            Logger.error(e)
        
    @training.post("/register/student")
    async def register_student(request: training_request_schemas.AddTrainingRegistration):

        # Find if training exists
        trainings = await TrainingModel.find_one(
            TrainingModel.training_id == request.training_id
        )

        if trainings is None:
            return JSONResponse(
                status_code = 404,
                content = {
                    "message" : "invalid training"
                }
            )
        
        student = TrainingRegistrations(**request.__dict__)

        db_response = await TrainingRegistrations.save(student)

        if db_response:
            send_email(request.student_email, "Training Registration", trainings)
            return JSONResponse(
                status_code = 200,
                content = {
                    "message" : "student registration completed"
                }
            )
        
        return JSONResponse(
            status_code = 500,
            content = {
                "message" : "student registration failed"
            }
        )


    @training.put("/update/training")
    async def update_training_details(request: Request):
        request = await request.json()

        trainings = await TrainingModel.find_one(
            TrainingModel.training_id == request["training_id"]
        )

        if trainings is None:
            return JSONResponse(
                status_code = 404,
                content = {
                    "message" : "training details not found"
                }
            )
        

        # Training details update
        trainings.training_name = request["training_name"]
        trainings.training_desc = request["training_desc"]
        trainings.training_venue = request["training_venue"]
        trainings.training_start_date = request["training_start_date"]
        trainings.training_end_date = request["training_end_date"]
        trainings.training_time = request["training_time"]
        trainings.trainer_name = request["trainer_name"]
        trainings.trainer_desc = request["trainer_desc"]

        db_response = await trainings.save()

        if db_response:
            return JSONResponse(
                status_code = 200,
                content = {
                    "message" : "training updated successfully"
                }
            )
        
        return JSONResponse(
            status_code = 500,
            content = {
                "message" : "training cannot be update"
            }
        )


    # TODO: test this later
    # def save_file(filename, data):
    #     base_path = path.abspath(path.dirname(path.dirname(__file__)))
        
    #     image_dir = path.join(base_path, '/images')

    #     with open(f"{image_dir}/{filename}", 'wb') as f:
    #         f.write(data)


    # TODO: Test this later
    # @training.post("/upload/avatar")
    # async def upload(file: UploadFile = File(...)):
        
    #     contents = await file.read()
    #     save_file(file.filename, contents)

    #     # Check if file is truely uploaded
    #     return JSONResponse(
    #         status_code = 200,
    #         content = {
    #             "message" : "avatar uploaded successfully"
    #         }
    #     )

    @training.delete("/delete")
    async def delete_training(request: Request):
        request = await request.json()

        trainings = await TrainingModel.find_one(
            TrainingModel.training_id == request["training_id"]
        )

        if trainings is not None:
            return JSONResponse(
                status_code = 404,
                content = {
                    "message" : "training details not found"
                }
            )
        
        db_response = await trainings.delete()

        if db_response:
            return JSONResponse(
                status_code = 200,
                content = {
                    "message" : "training deleted successfully"
                }
            )
        
        return JSONResponse(
            status_code = 500,
            content = {
                "message" : "training cannot be deleted"
            }
        )

    return training
