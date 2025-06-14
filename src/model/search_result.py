from src.model.application_pdf import ApplicationPDF
from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
from src.utils.regex import Regex, Summary

class SearchResult:
    def __init__(self, 
                applicant_profile: ApplicantProfile, 
                application_detail: ApplicationDetail,
                application_pdf: ApplicationPDF,
                matches: dict):
        self.applicant_profile = applicant_profile
        self.application_detail = application_detail
        self.pdf = application_pdf
        self.summary = Regex.extract_summary(self.pdf.cv_raw)
        self.matches = matches
