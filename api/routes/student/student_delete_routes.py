from api.drivers.student import student_drivers
from api.middlewares import authentication_middleware
from api.repository import student_repo
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from fastapi import APIRouter, Depends, status


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )


    @student.delete("/delete/arrdict", status_code=status.HTTP_200_OK)
    async def delete_company_letters(
            request: student_request_schemas.DeleteStudentArrayOfListSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        #TODO: give better route names
        
        """Handles company letter deletion to student's profile"""

        request = request.__dict__

        response = await student_repo.delete_to_array_of_dict(
            request, authorization
        )
        return response


    
    return student
