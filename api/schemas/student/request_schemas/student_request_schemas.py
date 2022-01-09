import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, validator


class RegisterStudentSchema(BaseModel):
    fname: str
    lname: str
    roll_no: str
    batch: int
    branch: str
    gender: str
    email: EmailStr
    phone: str
    password: str

    @validator('batch', always=True)
    def check_batch_le_current_year(cls, value):
        """Batch should not be greater than current year + 4"""
        
        todays_date = datetime.date.today()

        if((todays_date.year + 4) < value):
            raise ValueError("Batch greater than current year + 4 is not allowed")
        
        return value


    @validator('batch', always=True)
    def check_batch_lt_1994(cls, value):
        """Batch should not be less than year of establishment"""

        if(value < 1994):
            raise ValueError("Tezpur University did not exist before 1994")
        
        return value

    # @validator('password', always=True)
    # def check_batch_le_current_year(cls, value):
    #     todays_date = datetime.date.today()

    #     if((todays_date.year + 4) < value):
    #         raise ValueError("Batch greater than current year + 4 is not allowed")
        
    #     return value


    class Config:
        anystr_lower = True
        validate_assignment = True



class StudentPersonalInfoSchema(BaseModel):
    student_id: str
    fname: str
    lname: str
    roll_no: str
    batch: int
    branch: str
    gender: str
    email: EmailStr
    phone: str


    @validator('batch', always=True)
    def check_batch_le_current_year(cls, value):
        """Batch should not be greater than current year + 4"""
        
        todays_date = datetime.date.today()

        if((todays_date.year + 4) < value):
            raise ValueError("Batch greater than current year + 4 is not allowed")
        
        return value


    @validator('batch', always=True)
    def check_batch_lt_1994(cls, value):
        """Batch should not be less than year of establishment"""

        if(value < 1994):
            raise ValueError("Tezpur University did not exist before 1994")
        
        return value

    class Config:
        anystr_lower = True
        validate_assignment = True



class StudentAdditionalInfoSchema(BaseModel):
    student_id: str
    category: str
    minority: bool
    handicap: bool
    dob: str


class StudentEducationalInfoSchema(BaseModel):
    student_id: str
    matric_pcnt: float
    yop_matric: int
    hs_pcnt: float
    yop_hs: int
    sgpa: List[float]
    cgpa: float


class StudentAddressDetailsSchema(BaseModel):
    pincode: str
    state: str
    district: str
    country: str
    address_line_1: str
    address_line_2: Optional[str] = None


class StudentAddressInfoSchema(BaseModel):
    student_id: str
    permanent_address: StudentAddressDetailsSchema
    is_permanent_equals_present: bool
    present_address: StudentAddressDetailsSchema


class StudentCompanyInfoSchema(BaseModel):
    student_id: str
    current_company: str 
    current_role: str


class StudentCompanyLetterInfoSchema(BaseModel):
    student_id: str
    company_name: str
    letter_type: str
    letter_link: str
    is_verified: bool = False

class StudentCertificationInfoSchema(BaseModel):
    student_id: str
    course_name: str
    certificate_link: str
    is_verified: bool = False

class StudentScoreCardInfoSchema(BaseModel):
    student_id: str
    exam_name: str
    scorecard_link: str
    is_verified: bool = False

class StudentInternshipInfoSchema(BaseModel):
    student_id: str
    company_name: str
    internship_role: str
    start_date: datetime.date
    end_date: datetime.date

class StudentSocialInfoSchema(BaseModel):
    student_id: str
    platform_name: str
    profile_link: str
