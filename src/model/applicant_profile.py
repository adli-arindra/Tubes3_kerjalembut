from typing import List, Optional
from datetime import date

class ApplicantProfile:
    def __init__(self, 
            applicant_id: Optional[int] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            date_of_birth: Optional[date] = None,
            address: Optional[str] = None,
            phone_number: Optional[str] = None):
        self.applicant_id = applicant_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone_number = phone_number

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def __repr__(self):
        return (f"ApplicantProfile(applicant_id={self.applicant_id}, "
                f"first_name='{self.first_name}', "
                f"last_name='{self.last_name}', "
                f"date_of_birth={self.date_of_birth}, "
                f"address='{self.address}', "
                f"phone_number='{self.phone_number}')")