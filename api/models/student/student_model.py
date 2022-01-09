import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from beanie import (Document, Indexed, Insert, Replace, SaveChanges,
                    ValidateOnSave)
from beanie.odm.actions import before_event
from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel, Field, ValidationError


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
    batch: int #TODO: VALIDATOR --> Cannot be greater than current year + 4
    branch: str
    gender: str
    email: Indexed(str, unique=True) #TODO: VALIDATOR --> email validator
    phone: Optional[str] = None
    password: str #TODO: VALIDATOR --> check password strength
    
    # Additional info
    category: str = '' #TODO: VALIDATOR --> General, ST, SC etc
    minority: Optional[bool] = None
    handicap: Optional[bool] = None
    dob: str = '' #TODO: VALIDATOR --> Cannot be greater than current year - 16
    
    # Educational info
    matric_pcnt: Optional[float] = None #TODO: VALIDATOR --> Cannot be greater than 100
    yop_matric: Optional[int] = None #TODO: VALIDATOR --> Cannot be greater than current year
    hs_pcnt: Optional[float] = None #TODO: VALIDATOR --> Cannot be greater than 100
    yop_hs: Optional[int] = None #TODO: VALIDATOR --> Cannot be greater than current year
    sgpa: List[float] = [] #TODO: VALIDATOR --> Cannot be greater than 10
    cgpa: Optional[float] = None #TODO: VALIDATOR --> Cannot be greater than 10

    # Skills info
    skills: List[str] = [] 
    
    # Address info
    permanent_address: Optional[AddressModel] = {}
    is_permanent_equals_present: bool = False
    present_address: Optional[AddressModel] = None
    
    # Application info
    applications: Optional[List[PydanticObjectId]] = []
    
    # Company info
    current_company: Optional[str] = None #TODO: VALIDATOR --> Only valid if batch <= current year
    current_role: Optional[str] = None #TODO: VALIDATOR --> Only valid if batch <= current year
    
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


    @before_event([ValidateOnSave, Insert])
    async def to_lower(self):
        """Converts fields to lowercase. """

        fields: List[str] = [
            self.fname, 
            self.lname, 
            self.roll_no, 
            self.branch
        ]

        for field in fields:
            field = field.lower()


    @before_event([ValidateOnSave, Insert, SaveChanges, Replace])
    async def validate_fname(self):
        """fname should have atleast one letter. """

        if len(self.fname) < 1:
            raise ValueError("fname should contain atleast one letter")


    @before_event([ValidateOnSave, Insert, SaveChanges, Replace])
    async def validate_fname(self):
        """Password criterias: 
            --> Atleast 12 characters
            --> 1 uppercase letter, 1 lowercase letter
            --> 1 special character
            --> 1 digit
        """

        #TODO: write your password validator here


    class Settings:
        """Validates field values just before saving 
            the document to the database.
        """

        validate_on_save = True


    class Collection:
        name = "student"
