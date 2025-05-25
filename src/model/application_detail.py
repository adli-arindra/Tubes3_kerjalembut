from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class ApplicationDetail:
    detail_id: Optional[int] = None
    applicant_id: Optional[int] = None
    application_role: Optional[str] = None
    cv_path: Optional[str] = None