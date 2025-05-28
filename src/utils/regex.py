from typing import List, Optional

class Summary:
    def __init__(self,
                experience: Optional[List[str]] = None,
                education: Optional[List[str]] = None,
                skills: Optional[List[str]] = None,
                highlights: Optional[List[str]] = None,
                summary: Optional[str] = None,
                languages: Optional[List[str]] = None,
                certification: Optional[List[str]] = None):
        self.experience = experience if experience is not None else []
        self.education = education if education is not None else []
        self.skills = skills if skills is not None else []
        self.highlights = highlights if highlights is not None else []
        self.summary = summary
        self.languages = languages if languages is not None else []
        self.certification = certification if certification is not None else []

    def __repr__(self):
        return (f"Summary(\n"
                f"  experience={self.experience},\n"
                f"  education={self.education},\n"
                f"  skills={self.skills},\n"
                f"  highlights={self.highlights},\n"
                f"  summary='{self.summary}',\n"
                f"  languages={self.languages},\n"
                f"  certification={self.certification}\n"
                f")")

class Regex:
    @staticmethod
    def extract_summary(html: str) -> Summary:
        experience = Regex._extract_experience(html)
        education = Regex._extract_education(html)
        skills = Regex._extract_skills(html)
        highlights = Regex._extract_highlights(html)
        main_summary = Regex._extract_main_summary(html)
        languages = Regex._extract_languages(html)
        certification = Regex._extract_certification(html)

        return Summary(
            experience=experience,
            education=education,
            skills=skills,
            highlights=highlights,
            summary=main_summary,
            languages=languages,
            certification=certification
        )

    @staticmethod
    def _extract_experience(html: str) -> List[str]:
        return []

    @staticmethod
    def _extract_education(html: str) -> List[str]:
        return []

    @staticmethod
    def _extract_skills(html: str) -> List[str]:
        return []

    @staticmethod
    def _extract_highlights(html: str) -> List[str]:
        return []

    @staticmethod
    def _extract_main_summary(html: str) -> Optional[str]:
        return None

    @staticmethod
    def _extract_languages(html: str) -> List[str]:
        return []

    @staticmethod
    def _extract_certification(html: str) -> List[str]:
        return []