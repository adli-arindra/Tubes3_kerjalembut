from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class ApplicantProfile:
    applicant_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()