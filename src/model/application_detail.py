from typing import List, Optional
from datetime import date
import os
import io
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

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

    def get_cv_html(self) -> Optional[str]:
        if not self.cv_path:
            return None

        if not os.path.exists(self.cv_path):
            return None

        try:
            output_string = io.StringIO()
            with open(self.cv_path, 'rb') as in_file:
                extract_text_to_fp(in_file, 
                    output_string, laparams=LAParams(), 
                    output_type='html', codec='utf-8')
            
            html_content = output_string.getvalue()
            return html_content

        except Exception:
            return None
    
    def __repr__(self):
        return (f"ApplicationDetail(detail_id={self.detail_id}, "
                f"applicant_id={self.applicant_id}, "
                f"application_role='{self.application_role}', "
                f"cv_path='{self.cv_path}')")