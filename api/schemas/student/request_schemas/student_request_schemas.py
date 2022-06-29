import datetime
from optparse import Option
import pprint
import re

from typing import List, Optional
from urllib import response

from pydantic import AnyHttpUrl, BaseModel, EmailStr, root_validator, validator
from api.models.general_use_models import PydanticObjectId

from api.utils.company_profile_verifier import validate_company_profile
from api.drivers.student import student_drivers

class RegisterStudentSchema(BaseModel):
    student_id: str
    fname: str
    lname: str
    roll_no: str
    batch: int
    branch: str
    gender: str
    email: EmailStr
    phone: str
    password: str
    programme: str

    @validator('fname', always=True)
    def lower_fname(cls, value):
        """Lower the fname to save it in database"""
        
        return value.lower()

    @validator('lname', always=True)
    def lower_lname(cls, value):
        """Lower the lname to save it in database"""
        
        return value.lower()

    @validator('roll_no', always=True)
    def lower_roll_no(cls, value):
        """Lower the roll_no to save it in database"""
        
        return value.lower()

    @validator('branch', always=True)
    def lower_branch(cls, value):
        """Lower the branch to save it in database"""
        
        return value.lower()

    @validator('programme', always=True)
    def lower_programme(cls, value):
        """Lower the programme to save it in database"""
        
        return value.lower()

    @validator('gender', always=True)
    def lower_gender(cls, value):
        """Lower the gender to save it in the database"""

        return value.lower()

    @validator('email', always=True)
    def check_gmail(cls, value):
        "Only Gmail Account Allowed"

        if "@gmail.com" not in value.lower():
            raise ValueError("Only Gmail Account Allowed")

        return value.lower()
    
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

    @validator('password', always=True)
    def check_password(cls, value):
        '''
            Validates the password using regex
            Criteria:
                -> Password should be at least 8 characters long
                -> Password should have at least one uppercase letter
                -> Password should have at least one lowercase letter
                -> Password should have at least one digit
                -> Password should have at least one special character
        '''
        password_regex = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
        if not password_regex.match(value):
            raise ValueError("""Password should have at least one uppercase, one lowercase,
             one digit and one special character""")

        return value


    class Config:
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
    current_sem: str
    photo: Optional[str]

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

    @validator('phone', always=True)
    def check_phone_length(cls, value):
        """ phone number validation
            Criteria:
                -> Phone number should be of 10-13 digits
        """
        if not (10 <= len(value) <= 13):
            raise ValueError("Phone number should be of 10-13 digits")
        
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

    @validator('dob')
    def validate_dob(cls, value):
        """Validates date of birth of the student
            Criterias :  
                -> Student should be stleast 16 years old.
                -> Birth month should be less than or equal to 12.      
        """
        birth_date = value.split("/")
        birth_month, birth_year = int(birth_date[1]), int(birth_date[2])
        curr_date = datetime.date.today()

        if birth_month > 12 and birth_year > curr_date.year:
            raise ValueError("Date of birth is invalid")

        if birth_year > curr_date.year - 16 :
            raise ValueError("Year of birth is invalid")

        return value

class StudentCompetitiveExamInfoSchema(BaseModel):
    student_id: str
    name: str
    yop: Optional[int] = None
    id: str
    score: Optional[float] = None
    air: Optional[str] = None

class UpdateStudentCompetitiveExamInfoSchema(BaseModel):
    student_id: str
    type: str
    content: object
        
class StudentEducationalInfoSchema(BaseModel):
    student_id: str
    matric_pcnt: float
    yop_matric: int
    hs_pcnt: float
    yop_hs: int
    sgpa: List[float]
    cgpa: float
    jee_score: float
    jee_air: int

    @validator('matric_pcnt', always=True)
    def check_matric_pcnt_lt_100(cls, value):
        """Percentage of Matric should be less than 100 and greater than 0"""
        if(value > 100 or value < 0):
            raise ValueError("Percentage of Matric should be less than 100 and greater than 0")
        
        return value

    @validator('hs_pcnt', always=True)
    def check_hs_pcnt_lt_100(cls, value):
        """Percentage of HS should be less than 100 and greater than 0"""
        if(value > 100 or value < 0):
            raise ValueError("Percentage of HS should be less than 100 and greater than 0")
        
        return value

    @validator('yop_hs', always=True)
    def check_yop_hs(cls, value):
        """Year of passing of HS should be less than current year and greater than matric year"""
        if(value > datetime.date.today().year):
            raise ValueError("Year of passing of HS should be less than current year")

        return value

    @validator('yop_hs', always=True)
    def check_yop_hs_gt_matric_yop(cls, value, values):
        if(value < values["yop_matric"]):
            raise ValueError("Year of passing of HS should be greater than matric year")
            
        return value

    @validator('sgpa', always=True)
    def validate_sgpa(cls, value):
        """Validates SGPA of the student
            Criterias :  
                -> SGPA should be between 0 and 10.
        """
        for sgpa in value:
            if(sgpa < 0 or sgpa > 10):
                raise ValueError("SGPA is invalid")
        
        return value

    @validator('cgpa', always=True)
    def validate_cgpa(cls, value):
        """Validates CGPA of the student
            Criterias :  
                -> CGPA should be between 0 and 10.
        """
        if(value < 0 or value > 10):
            raise ValueError("CGPA is invalid")
        
        return value

    @validator('jee_score', always=True)
    def validate_jee_score(cls, value):
        """Validates JEE score of the student
            Criterias :  
                -> JEE score should be between 0 and 100.
        """
        if(value < 0 or value > 100):
            raise ValueError("JEE score is invalid")
        
        return value

class StudentAddressFormat(BaseModel):
    pincode: str
    state: str
    district: str
    city: str
    country: str
    address_line_1: str
    address_line_2: Optional[str] = None


class StudentAddressInfoSchema(BaseModel):
    student_id: str
    permanent_address: StudentAddressFormat
    is_permanent_equals_present: bool
    present_address: Optional[StudentAddressFormat] = None


    @root_validator(pre=True)
    def validate_addresses(cls, values):
        """Checks if is_permanent_equals_present is true,
            then present_address will be empty,
            else will be valid dictionary
        """
        if (values["is_permanent_equals_present"] and 
            values["present_address"] is not None):

                values["present_address"] = None


        if (not values["is_permanent_equals_present"] and 

            not values["present_address"]):

                raise ValueError("present address should be present when permanent address and present address are not same")
        

        return values


class NotificationInfoSchema(BaseModel):
    notification_header: str
    notification_body: str


class StudentCompanyLetterInfoSchema(BaseModel):
    student_id: str
    company_name: str
    letter_type: str
    letter_link: str

class StudentOfferLetterInfoSchema(BaseModel):
    student_id: str
    name: str
    link: str

class StudentPlacementFormat(BaseModel):
    company_name: str
    designation: str
    salary: str
    offer_link: str

class StudentJobInfoSchema(BaseModel):
    student_id: str
    job_type: str
    job_info: Optional[StudentPlacementFormat]
    internship_info: Optional[StudentPlacementFormat]  

class StudentHigherStudiesFormat(BaseModel):
    programme: str  
    branch: str
    institution: str
    exam_cleared: str
    institution_id: str
    fellowship: str
    offer_link: str

class StudentHigherStudiesInfoSchema(BaseModel):
    student_id: str
    higher_studies: Optional[StudentHigherStudiesFormat]

class StudentCertificationInfoSchema(BaseModel):
    student_id: str
    course_name: str
    certificate_link: str


class StudentScoreCardInfoSchema(BaseModel):
    student_id: str
    exam_name: str
    scorecard_link: str


class StudentJobExperienceInfoSchema(BaseModel):
    student_id: str
    company_name: str
    employment_type: str
    role: str
    is_current_company: bool = False
    start_month: int
    start_year: int
    end_month: Optional[int] = None
    end_year: Optional[int] = None

    @validator('company_name',always=True)
    def validate_company_name(cls, value):
        return validate_company_profile(company=value)

    
    @validator('employment_type', always=True)
    def is_employment_type_valid(cls, value):
        """
            Validates the employment type
            Criteria:
                -> Roles have to be from the mentioned ones.
        """
        roles = [
            'internship', 'full-time', 'freelance', 'part-time'
        ]

        if value.lower() not in roles:
            raise ValueError(f'{value} employment type does not exist')

        return value

    
    @root_validator(pre=True)
    def validate_work_period(cls, values):
        """
            Validates work period in the company
            Criteria:
                -> If the current company is true then end date has to be none.
                -> start date have to be before end date
                -> end date have to be before current date
        """
        curr_date = datetime.date.today()

        if values["start_month"] is None or values["start_year"] is None:
            raise ValueError("start month and start year are required fields")

        if values["start_month"] > 12 or values["start_month"] < 1:
            raise ValueError("start month have to be between 1 and 12")

        if values["is_current_company"] :
            values["end_month"] = None
            values["end_year"] = None

        if values["start_month"] > curr_date.month and values["start_year"] >= curr_date.year :
                raise ValueError("start date should not be after current date")

        if not values["is_current_company"]:

            if values["end_month"] is None or values["end_year"] is None:
                raise ValueError("end month and end year are required fields")

        
            if values["end_month"] > 12 or values["end_month"] < 1:
                raise ValueError("end month have to be between 1 and 12")

            if values["end_month"] > curr_date.month and values["end_year"] >= curr_date.year :
                raise ValueError("end date should not be after current date")

            if values["start_month"] > values["end_month"] and values["start_year"] >= values["end_year"] :
                raise ValueError("start date should not be after end date")

        return values


class StudentSocialInfoSchema(BaseModel):
    student_id: str
    platform_name: str
    profile_link: AnyHttpUrl

    @validator('profile_link',always=True)
    def validate_platform(cls, value):
        """
            Validate Social Platform
            Criteria:
                -> The domain name of the platform link should not be from the 
                    listed out social media platforms
        """

    #TODO: Check same platform should not be entered twice 

    @validator('platform_name', always=True)
    async def check_if_platform_exist(cls, value):
        student_prev_skill = await student_drivers.Student().get_student_social(cls.student_id)
        if student_prev_skill:
            for prev_skill in student_prev_skill:
                if prev_skill["platform_name"] == value:
                    raise ValueError("Platform already exist")
        return True


    #TODO: Optimise the code, failing on testcases
    @validator('platform_name', always=True)
    def check_if_isblacklisted(cls, value):
        try:
            blacklist_platforms = [
                    'instagram', 'snapchat', 'discord', 'tiktok', 'sharechat', 't.me',
                    'pinterest', 'reddit', 'facebook', 'tinder', 'mxtakatak'
                ]

            domain_by_dot = value.split('.')[1]
            print(domain_by_dot)

            if domain_by_dot.lower() in blacklist_platforms:
                raise ValueError(f"{value} platform is not accepted")


            domain_by_slash = value.split('//')[1].split('.')[0]
            print(domain_by_slash)
            if domain_by_slash.lower() in blacklist_platforms:
                raise ValueError(f"{value} platform is not accepted")
                
        except Exception as e:
                raise ValueError(f"{value} platform is not accepted")


class DeleteStudentArrayOfListSchema(BaseModel):
    student_id: str
    model_type: str
    uid: str

    @validator('model_type', always=True)
    def validate_model_type(cls, value):
        #TODO: Add descriptive doc string

        model_type = [
            "company_letters",
            "job_experience",
            "certifications",
            "score_cards",
            "social_links",
            "notifications",
        ]

        if value not in model_type:
            raise ValueError(f"model_type {value} is not a valid value, choose from {model_type}")
        
        return value

class UpdateStudentSkillsSchema(BaseModel):

    student_id : str
    skills : List[str]

    @validator("skills")
    def validate_events(value):
    #TODO : add suitable doc string

        if len(value) == 0 :
            raise ValueError("skills list should never be empty")

        return value

class UpdateStudentPasswordSchema(BaseModel):
    student_id : str
    password : str

    @validator("password")
    def validate_password(value):
        '''
            Validates the password using regex
            Criteria:
                -> Password should be at least 8 characters long
                -> Password should have at least one uppercase letter
                -> Password should have at least one lowercase letter
                -> Password should have at least one digit
                -> Password should have at least one special character
        '''
        password_regex = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
        if not password_regex.match(value):
            raise ValueError("""Password should have at least one uppercase, one lowercase,
             one digit and one special character""")

        return value
