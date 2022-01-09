import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from beanie import (Document, Indexed, Insert, Replace, SaveChanges,
                    ValidateOnSave)
from beanie.odm.actions import before_event
from bson.objectid import ObjectId as BsonObjectId
from pydantic import (BaseModel, Field, ValidationError, root_validator,
                      validator)
from pydantic.types import confloat, conint, conlist
from email_validator import EmailNotValidError, validate_email


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

    current_year = datetime.datetime.now().year

    is_account_active: bool = False
    is_banned: bool = False
    token: Optional[str] = ''
    student_id: str = str(uuid4())
    
    # Personal info 
    fname: str
    lname: Optional[str] = None
    roll_no: Indexed(str, unique=True)
    batch: conint(ge=2010, le=current_year+4)
    branch: str
    gender: str
    email: Indexed(str, unique=True) #TODO: VALIDATOR --> email validator
    phone: Optional[str] = None
    password: str
    
    # Additional info
    category: str = ''
    minority: Optional[bool] = None
    handicap: Optional[bool] = None
    dob: str = '' #TODO: VALIDATOR --> Cannot be greater than current year - 16
    
    # Educational info
    matric_pcnt: Optional[confloat(ge=0, le=100)] = None
    yop_matric: Optional[conint(ge=2005, le=current_year)] = None
    hs_pcnt: Optional[confloat(ge=0, le=100)] = None
    yop_hs: Optional[conint(ge=2005, le=current_year)] = None
    sgpa: conlist(int, min_items=0, max_items=10) = []
    cgpa: Optional[confloat(ge=0, le=10)] = None

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

    @root_validator(pre=True)
    def to_lower(cls, values):
        """Convert all keys to lower case."""
        
        fields: List[str] = [
            values['fname'],
            values['lname'],
            values['roll_no'],
            values['branch']
        ]

        for field in fields:
            field = field.lower()

    @validator('fname')
    def fname_validator(cls, fname):
        """fname should have atleast one letter. """

        if len(fname) < 1:
            raise ValueError("fname should contain atleast one letter")
        return fname

    @validator('password')
    def validate_password(cls, password):
        schar = '[@_!#$%^&*()<>?/\|}{~:]'.split('')

        lower = upper = special_char = digit = False
        
        is_invalid = True
       
        if len(password) < 12:
            raise ValueError("password should be atleast of length 12")
        
        for i in password:
        
            # checking for presence of lowercase alphabets 
            if not lower and i.islower():
                lower = True         
        
            # checking for presence of uppercase alphabets
            elif not upper and i.isupper():
                upper = True           
        
            # checking for presence of digits
            elif not digit and i.isdigit():
                digit = True           
        
            # checking for special characters
            elif not special_char and (i in schar):  
                special_char = True
 
            else:
                is_invalid = False
                break
                      
        if is_invalid:
            raise ValueError('invalid password')

    @validator('category')
    def validate_category(cls, category):
        """Validates category. """

        categories = ['General', 'EWS', 'ST', 'SC', 'OBC']

        if category not in categories:
            raise ValueError(f"Category should be one of {categories}")

    @validator('email')
    def validate_email(cls, email):
        """Validates email"""

        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValueError("Invalid email")

    class Settings:
        """Validates field values just before saving 
            the document to the database.
        """

        validate_on_save = True


    class Collection:
        name = "student"
