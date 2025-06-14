class ApplicationPDF:
    def __init__(self, detail_id: int, cv_text: str, cv_raw: str):
        self.detail_id = detail_id
        self.cv_text = cv_text
        self.cv_raw = cv_raw

    def __repr__(self):
        return f"ApplicationPDF(detail_id={self.detail_id}, cv_text={self.cv_text}, cv_raw=[{len(self.cv_raw)} chars])"
