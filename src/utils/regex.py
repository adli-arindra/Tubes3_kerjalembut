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

import re


class Regex:
    _HEADERS = [
        "experience",
        "education",
        "skills",
        "highlights",
        "summary",
        "languages",
        "certification",
        "accomplishments",
    ]

    @staticmethod
    def extract_summary(html: str) -> Summary:
        cleaned = Regex._clean_text(html)

        experience = Regex._extract_experience(cleaned)
        education = Regex._extract_education(cleaned)
        skills = Regex._extract_skills(cleaned)
        highlights = Regex._extract_highlights(cleaned)
        main_summary = Regex._extract_main_summary(cleaned)
        languages = Regex._extract_languages(cleaned)
        certification = Regex._extract_certification(cleaned)

        return Summary(
            experience=experience,
            education=education,
            skills=skills,
            highlights=highlights,
            summary=main_summary,
            languages=languages,
            certification=certification,
        )

    @staticmethod
    def _clean_text(html: str) -> str:
        text = re.sub(r"<[^>]+>", "\n", html)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"\r", "", text)
        text = re.sub(r" +", " ", text)
        text = re.sub(r"\n+", "\n", text)
        return text.strip()

    @staticmethod
    def _get_section(text: str, header: str) -> str:
        other_headers = [h for h in Regex._HEADERS if h.lower() != header.lower()]
        pattern = rf"(?im)^\s*{re.escape(header)}\s*(.+?)(?=^\s*(?:{'|'.join(map(re.escape, other_headers))})\s*$|\Z)"
        match = re.search(pattern, text, flags=re.S | re.M)
        if match:
            return match.group(1).strip()
        return ""

    @staticmethod
    def _split_lines(section: str) -> List[str]:
        return [line.strip(" -") for line in section.splitlines() if line.strip()]

    @staticmethod
    def _extract_experience(text: str) -> List[str]:
        section = Regex._get_section(text, "experience")
        return Regex._split_lines(section)

    @staticmethod
    def _extract_education(text: str) -> List[str]:
        section = Regex._get_section(text, "education")
        return Regex._split_lines(section)

    @staticmethod
    def _extract_skills(text: str) -> List[str]:
        section = Regex._get_section(text, "skills")
        return Regex._split_lines(section)

    @staticmethod
    def _extract_highlights(text: str) -> List[str]:
        section = Regex._get_section(text, "highlights")
        return Regex._split_lines(section)

    @staticmethod
    def _extract_main_summary(text: str) -> Optional[str]:
        section = Regex._get_section(text, "summary")
        lines = Regex._split_lines(section)
        if lines:
            return " ".join(lines)
        return None

    @staticmethod
    def _extract_languages(text: str) -> List[str]:
        section = Regex._get_section(text, "languages")
        return Regex._split_lines(section)

    @staticmethod
    def _extract_certification(text: str) -> List[str]:
        section = Regex._get_section(text, "certification")
        return Regex._split_lines(section)
