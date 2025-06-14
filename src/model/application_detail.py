from typing import List, Optional
from datetime import date
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from src.utils.pdf_reader import PDFReader

class ApplicationDetail:
    def __init__(
            self, 
            detail_id: Optional[int] = None, 
            applicant_id: Optional[int] = None, 
            application_role: Optional[str] = None, 
            cv_path: Optional[str] = None):
        self.detail_id = detail_id
        self.applicant_id = applicant_id
        self.application_role = application_role
        self.cv_path = cv_path

        self.cv_text = PDFReader.read_raw(self.cv_path)
        self.cv_raw = PDFReader.read_text(self.cv_path)

    def __repr__(self):
        return (f"ApplicationDetail(detail_id={self.detail_id}, "
                f"applicant_id={self.applicant_id}, "
                f"application_role='{self.application_role}', "
                f"cv_path='{self.cv_path}')")