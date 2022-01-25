import datetime
import pprint
from typing import List, Optional

import requests
from pydantic import AnyHttpUrl, BaseModel, EmailStr, root_validator, validator


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

    @validator('dob')
    def validate_dob(cls, value):
        """Validates date of birth of the student
            Criterias :  
                -> Student should be stleast 16 years old.
                -> Birth month should be less than or equal to 12.      
        """
        birth_date = value.split("/")
        birth_month, birth_year = int(birth_date[0]), int(birth_date[1])
        curr_date = datetime.date.today()

        if birth_month > 12 and birth_year > curr_date.year:
            raise ValueError("Date of birth is invalid")

        if birth_year < curr_date.year - 16 :
            raise ValueError("Year of birth is invalid")

        return value


class StudentEducationalInfoSchema(BaseModel):
    student_id: str
    matric_pcnt: float
    yop_matric: int
    hs_pcnt: float
    yop_hs: int
    sgpa: List[float]
    cgpa: float


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
        print(values)

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
        """Validates compnay name
            Criteria:
                -> Company should have it's own page on LinkedIn    
        """

        company = value.replace(' ','').lower()
        url = f"https://www.linkedin.com/company/{company}"

        payload={}
        headers = {
            'authority': 'www.linkedin.com',
            'method': 'GET',
            'path': '/company/verizon/',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'li_sugr=a9ec4480-7d0c-4845-95e7-39605d64191e; bcookie="v=2&8aaee4d9-dae2-4557-8982-764a1c4d8220"; bscookie="v=1&2022011215585042776796-5cc9-45a6-8cc5-81319174ccc1AQE_17iC6_72LTD8_p-00jJCspROFjDQ"; lang=v=2&lang=en-us; _gcl_au=1.1.417085013.1642018060; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=15799541411558395992045813087850080675; li_rm=AQFw0wobjO2NlAAAAX5P55PV9VBojDJkqKhl_YRquLswhB18wxW5CrzlKEbyd4a5Pkzg4sK4titxilH1vTM4uvdtNP51lhhdj3SPrI211t6J-s-eGf37cdyS; li_at=AQEDASpjhLADRqWwAAABfk_nnOUAAAF-c_Qg5U4Avoa3chQYq0gbZXsytq09SlpZZBggeNaQsXJ02AQ5fAJyV5Yq9vn0rTQoAszAKcsdg6bsVo-UHJcwisQGyxpLp3mVYESTXOa5hPbmf6Ba5Hr6g389; liap=true; JSESSIONID="ajax:8815064273025167449"; timezone=Asia/Calcutta; _guid=271bb573-1864-4058-8892-8bd0c8593a8d; AnalyticsSyncHistory=AQK2_sag26JQDQAAAX5P561HnSsDCdtE74-2dCE4vAO3tTg5oP08xO1DW6TitJ7n2Ipoaqxx28Rp0e9i3psPlw; lms_ads=AQGJAFOpD7Ij8gAAAX5P56_xR2RnnpHvzV7PrTt1XFYLLXOfaxm1c1IMWHrXs3fIiVy_5jZxQFCG_Pndonz85bkJkm3flnGG; lms_analytics=AQGJAFOpD7Ij8gAAAX5P56_xR2RnnpHvzV7PrTt1XFYLLXOfaxm1c1IMWHrXs3fIiVy_5jZxQFCG_Pndonz85bkJkm3flnGG; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19005%7CMCMID%7C15228333244831983722065779036496648808%7CMCAAMLH-1642622895%7C12%7CMCAAMB-1642622895%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1642025295s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1805256044; pushPermState=default; UserMatchHistory=AQLX2VHUilNAGwAAAX5P7lNyoyxI9B84M8tf13u_SiN_IALpIUauE4yazo3Yufm_9LPkgAVn5VKMyMyhVUnY--bfSKzs3qsmM5rpP8p3d5--TLfiH1L7Yyr2FR2_AMrXURSzCgljGCNQXLQWtVy-yCYWZDkMD2IUaQP3HgVRVeioZkFsv46lBt_dzTqC5klUJUnRP7ywn60Zf_rLko6RJC-roHh9Zm87U4CXLndy15uCcrxDZtWj19oTx_C0U1qlOtZfZVieqKpd3n5WXCofxwi6EUbA_NQ2y5onENU; lidc="b=TB04:s=T:r=T:a=T:p=T:g=3867:u=732:x=1:i=1642018527:t=1642019932:v=2:sig=AQHV6hl79LViOd9L81EeA8aNCM1Ux1vn"; bcookie="v=2&fea97cf7-1aaf-4164-84b4-c7d2286b72bd"; lidc="b=TB04:s=T:r=T:a=T:p=T:g=3867:u=732:x=1:i=1642018814:t=1642019932:v=2:sig=AQG-TOHFdLb9PiOMqYMs9mRF2YMb0JDF"',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload).status_code

        if response != 200:
            # TODO: Sent a notification to admin
            raise ValueError(f"{value} company is not verified.")
        return value

    
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
        #TODO: Optimise the code, failing on testcases

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

            return value
            
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
        #TODO : write a suitable password validator
        pass