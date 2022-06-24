from optparse import Option
from typing import Any, Dict, List

from api.models.student.student_model import *
from pydantic import BaseModel

from api.schemas.student.request_schemas.student_request_schemas import StudentHigherStudiesInfoSchema


class AuthorizedUserStudentProfileView(BaseModel):

    events: List[str]
    
    student_id: str
    # Personal info 
    fname: str
    lname: str
    roll_no: str
    batch: int 
    branch: str
    gender: str
    email: str
    phone: str
    password: str
    current_sem: str 
    photo: Optional[str]
    
    # Additional info
    category: str
    minority: Optional[bool]
    handicap: Optional[bool]
    dob: str = '' 

    # Educational info
    matric_pcnt: Optional[float]
    yop_matric: Optional[int]
    hs_pcnt: Optional[float]
    yop_hs: Optional[int]
    sgpa: List[float]
    cgpa: Optional[float]
    jee_score: Optional[float]
    jee_air: Optional[str]

    # Skills info
    skills: List[Any] = [] 
    
    # Address info
    permanent_address: Optional[AddressModel] = {}
    is_permanent_equals_present: bool
    present_address: Optional[AddressModel]

    #Competitive Exam info
    competitive_exams: Optional[List[CompetitiveExamModel]]
    
    # Company Letters info
    company_letters: Optional[List[CompanyLetterModel]]

    offer_letters: Optional[List[OfferLetterModel]]

    higher_studies: Optional[StudentHigherStudentModel]
    
    # Job Info
    job_type: str
    job_info: Optional[JobModel]
    internship_info: Optional[JobModel]

    # Application info
    applied_positions: Optional[List[PydanticObjectId]] = []

    # Job experience info
    job_experience: List[JobExperienceModel]
    
    # Certification info
    certifications: Optional[List[CertificationModel]]
    
    # Score card info
    score_cards: Optional[List[ScorecardModel]]
    
    # Social info
    social_links: Optional[List[SocialModel]]



class UnauthorizedUserStudentProfileView(BaseModel):
    
    # Personal info 
    fname: str
    lname: str
    roll_no: str
    batch: int 
    branch: str
    gender: str
    email: str
    
    # Additional info
    category: str
    minority: Optional[bool]
    handicap: Optional[bool]

    # Educational info
    matric_pcnt: Optional[float]
    yop_matric: Optional[int]
    hs_pcnt: Optional[float]
    yop_hs: Optional[int]
    sgpa: List[float]
    cgpa: Optional[float]

    # Skills info
    skills: List[Any] = [] 

    # Job experience info
    job_experience: List[JobExperienceModel]
    
    # Certification info
    certifications: Optional[List[CertificationModel]]
    
    # Score card info
    score_cards: Optional[List[ScorecardModel]]
    
    # Social info
    social_links: Optional[List[SocialModel]]

class adminProfileView(BaseModel):

    events: List[str]
    
    # Personal info 
    fname: str
    lname: str
    roll_no: str
    batch: int 
    branch: str
    gender: str
    email: str
    phone: str

class AdminDataSaveView(BaseModel):

    fname: str
    lname: str
    roll_no: str
    batch: int 
    branch: str
    gender: str
    email: str
    phone: str

    # Educational info
    matric_pcnt: Optional[float]
    yop_matric: Optional[int]
    hs_pcnt: Optional[float]
    yop_hs: Optional[int]