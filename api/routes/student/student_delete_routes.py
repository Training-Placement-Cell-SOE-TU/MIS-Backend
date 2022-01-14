from api.drivers.student import student_drivers
from api.middlewares import authentication_middleware
from api.repository import student_repo
from api.schemas.student.request_schemas import student_request_schemas
from api.utils.exceptions import exceptions
from fastapi import APIRouter, Depends, status, Request


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )


    @student.delete("/delete/arrdict", status_code=status.HTTP_200_OK)
    async def delete_company_letters(
            request: Request,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        #TODO: give better route names
        
        """Handles company letter deletion to student's profile"""

        request = await request.json()

        model_type = "company_letters"

        response = await student_repo.delete_to_array_of_dict(
            request, authorization, model_type
        )
        return response



    @student.delete("/add/experience", status_code=status.HTTP_200_OK)
    async def delete_experience(
            request: student_request_schemas.StudentJobExperienceInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles job experience deletion to student schema"""

        model_type = "job_experience"

        response = await student_repo.delete_to_array_of_dict(
            request, authorization, model_type
        )
        return response



    @student.delete("/add/certification", status_code=status.HTTP_200_OK)
    async def delete_certifications(
            request: student_request_schemas.StudentCertificationInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles certification deletion to student schema"""

        model_type = "certifications"

        response = await student_repo.delete_to_array_of_dict(
            request, authorization, model_type
        )
        return response



    @student.delete("/add/scorecard", status_code=status.HTTP_200_OK)
    async def delete_scorecards(
            request: student_request_schemas.StudentScoreCardInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles score card deletion to student schema"""

        model_type = "score_cards"

        response = await student_repo.delete_to_array_of_dict(
            request, authorization, model_type
        )
        return response

        

    @student.delete("/add/social", status_code=status.HTTP_200_OK)
    async def delete_social_links(
            request: student_request_schemas.StudentSocialInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles social profile deletion to student's profile"""

        model_type = "social_links"

        response = await student_repo.delete_to_array_of_dict(
            request, authorization, model_type
        )
        return response

    
    return student