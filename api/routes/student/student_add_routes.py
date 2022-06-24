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



    @student.post("/add/letters", status_code=status.HTTP_200_OK)
    async def add_company_letters(
            request: student_request_schemas.StudentCompanyLetterInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles company letter addition to student's profile"""

        model_type = "company_letters"

        response = await student_repo.add_to_array_of_dict(
            request, authorization, model_type
        )
        return response



    @student.post("/add/experience", status_code=status.HTTP_200_OK)
    async def add_experience(
            request: student_request_schemas.StudentJobExperienceInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles job experience addition to student schema"""

        model_type = "job_experience"

        response = await student_repo.add_to_array_of_dict(
            request, authorization, model_type
        )
        return response



    @student.post("/add/certification", status_code=status.HTTP_200_OK)
    async def add_certifications(
            request: student_request_schemas.StudentCertificationInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles certification addition to student schema"""

        model_type = "certifications"

        response = await student_repo.add_to_array_of_dict(
            request, authorization, model_type
        )
        return response



    @student.post("/add/scorecard", status_code=status.HTTP_200_OK)
    async def add_scorecards(
            request: student_request_schemas.StudentScoreCardInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles score card addition to student schema"""

        model_type = "score_cards"

        response = await student_repo.add_to_array_of_dict(
            request, authorization, model_type
        )
        return response

    @student.post("/add/offer", status_code=status.HTTP_200_OK)
    async def add_offer_letter(
            request: student_request_schemas.StudentOfferLetterInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
    ):
        """Handles offer letter addition to student schema"""

        model_type = "offer_letters"

        response = await student_repo.add_to_array_of_offers(
            request, authorization, model_type
        )
        return response
        

    @student.post("/add/social", status_code=status.HTTP_200_OK)
    async def add_social_links(
            request: student_request_schemas.StudentSocialInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
        
        """Handles social profile addition to student's profile"""

        model_type = "social_links"

        response = await student_repo.add_to_array_of_dict(
            request, authorization, model_type
        )
        return response

    @student.post("/add/exams", status_code=status.HTTP_200_OK)
    async def add_competitive_exams(
            request: student_request_schemas.StudentCompetitiveExamInfoSchema,
            authorization = Depends(authentication_middleware.is_authenticated)
        ):
            
            """Handles competitive exams addition to student's profile"""
    
            model_type = "competitive_exams"
            print(request)
    
            response = await student_repo.add_to_array_of_dict(
                request, authorization, model_type
            )
            
            return response
    
    return student
