from api.models.student.student_model import *
from api.models.general_use_models import NotificationModel

model_mappings = {
    "company_letters" : CompanyLetterModel,
    "job_experience" : JobExperienceModel,
    "certifications" : CertificationModel,
    "score_cards": ScorecardModel,
    "social_links": SocialModel,
    "notifications": NotificationModel,
    "competitive_exams": CompetitiveExamModel,
    "offer_letters": OfferLetterModel,
}