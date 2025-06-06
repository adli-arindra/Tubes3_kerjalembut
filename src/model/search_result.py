from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
from src.controller.regex import Regex, Summary

class SearchResult:
    def __init__(self, 
                applicant_profile: ApplicantProfile, 
                application_detail: ApplicationDetail):
        self.applicant_profile = applicant_profile
        self.application_detail = application_detail
        self.summary = Regex.extract_summary(self)
