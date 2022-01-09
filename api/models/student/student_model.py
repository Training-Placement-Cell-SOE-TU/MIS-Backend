import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from beanie import Document, Indexed
from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel, EmailStr, Field


class CompanyLetterModel(BaseModel):
    """Company Letters Model"""

    company_name: str
    letter_type: str
    letter_link: str
    is_verified: bool = False


class InternshipModel(BaseModel):
    """Internship Model"""

    company_name: str
    internship_role: str
    start_date: datetime.date
    end_date: datetime.date

class CertificationModel(BaseModel):
    """Certifications Model"""

    course_name: str
    certificate_link: str
    is_verified: bool = False


class ScorecardModel(BaseModel):
    """Scorecard Model"""

    exam_name: str
    scorecard_link: str
    is_verified: bool = False


class SocialModel(BaseModel):
    """Social Media Platform Model"""

    platform_name: str
    profile_link: str

class AddressModel(BaseModel):
    """Address Model"""

    pincode: str = ''
    state: str = ''
    district: str = ''
    country: str = ''
    address_line_1: str = ''
    address_line_2: Optional[str] = None


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class StudentModel(Document):
    """Maps student model to database document. """

    # Extra functionality use fields
    is_account_active: bool = False
    is_banned: bool = False
    token: Optional[str] = ''
    student_id: str = str(uuid4())
    
    # Personal info 
    fname: str
    lname: Optional[str] = None
    roll_no: Indexed(str, unique=True)
    batch: int 
    branch: str
    gender: str
    email: Indexed(str, unique=True) 
    phone: Optional[str] = None
    password: str 
    
    # Additional info
    category: str = '' 
    minority: Optional[bool] = None
    handicap: Optional[bool] = None
    dob: str = '' 

    # Educational info
    matric_pcnt: Optional[float] = None 
    yop_matric: Optional[int] = None 
    hs_pcnt: Optional[float] = None 
    yop_hs: Optional[int] = None 
    sgpa: List[float] = [] 
    cgpa: Optional[float] = None 

    # Skills info
    skills: List[str] = [] 
    
    # Address info
    permanent_address: Optional[AddressModel] = {}
    is_permanent_equals_present: bool = False
    present_address: Optional[AddressModel] = None
    
    # Application info
    applications: Optional[List[PydanticObjectId]] = []
    
    # Company info
    current_company: Optional[str] = None 
    current_role: Optional[str] = None 
    
    # Company Letters info
    company_letters: Optional[List[CompanyLetterModel]] = None
    
    # Internship info
    internship: List[InternshipModel] = []
    
    # Certification info
    certifications: Optional[List[CertificationModel]] = None
    
    # Score card info
    score_cards: Optional[List[ScorecardModel]] = None
    
    #Social info
    social_links: Optional[List[SocialModel]] = None



    class Config:
        anystr_lower = True
        

    class Collection:
        name = "student"
