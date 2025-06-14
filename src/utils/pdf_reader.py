import os
import io
from typing import Optional
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

class PDFReader:
    @staticmethod
    def read_raw(pdf_path: str) -> Optional[str]:
        if not os.path.exists(pdf_path):
            return None

        try:
            output = io.BytesIO()
            with open(pdf_path, 'rb') as f:
                extract_text_to_fp(
                    f, output,
                    laparams=LAParams(),
                    output_type='html',
                    codec='utf-8'
                )
            return output.getvalue().decode('utf-8')
        except Exception as e:
            print(f"[ERROR] read_raw failed on {pdf_path}: {e}")
            return None

    @staticmethod
    def read_text(pdf_path: str) -> Optional[str]:
        if not os.path.exists(pdf_path):
            return None

        try:
            output = io.StringIO()
            with open(pdf_path, 'rb') as f:
                extract_text_to_fp(
                    f, output,
                    laparams=LAParams(),
                    output_type='text',
                    codec='utf-8'
                )
            return output.getvalue()
        except Exception:
            return None
