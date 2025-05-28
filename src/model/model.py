from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
from src.model.search_result import SearchResult

class Model:
    def __init__(self, 
                applicant_profiles: list[ApplicantProfile], 
                application_details: list[ApplicationDetail]) -> None:
        self.applicant_profiles = applicant_profiles
        self.application_details = application_details
    
    def match_exact(self, algorithm: str) -> list[SearchResult]:
        match algorithm:
            case "kmp":
                pass
            case "bm":
                pass
            case "ac":
                pass
    
    def match_fuzzy(self) -> list[SearchResult]:
        pass