from typing import List, Optional
import re


class Summary:
    def __init__(
        self,
        experience: Optional[List[str]] = None,
        education: Optional[List[str]] = None,
        skills: Optional[List[str]] = None,
        highlights: Optional[List[str]] = None,
        summary: Optional[str] = None,
        languages: Optional[List[str]] = None,
        certification: Optional[List[str]] = None,
    ):
        self.experience = experience if experience is not None else []
        self.education = education if education is not None else []
        self.skills = skills if skills is not None else []
        self.highlights = highlights if highlights is not None else []
        self.summary = summary
        self.languages = languages if languages is not None else []
        self.certification = certification if certification is not None else []

    def __repr__(self):
        return (
            "Summary(\n"
            f"  experience={self.experience},\n"
            f"  education={self.education},\n"
            f"  skills={self.skills},\n"
            f"  highlights={self.highlights},\n"
            f"  summary='{self.summary}',\n"
            f"  languages={self.languages},\n"
            f"  certification={self.certification}\n"
            ")"
        )


class Regex:
    # ------------------------------------------------------------------
    # Static configuration
    # ------------------------------------------------------------------
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

    # whitelist is lower‑cased for O(1) look‑ups
    _ALLOWED_SKILLS = {
        s.lower()
        for s in {
            "python",
            "java",
            "javascript",
            "react",
            "angular",
            "vue",
            "node.js",
            "express",
            "sql",
            "mysql",
            "postgresql",
            "mongodb",
            "redis",
            "html",
            "css",
            "bootstrap",
            "git",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "linux",
            "windows",
            "excel",
            "powerpoint",
            "word",
            "photoshop",
            "illustrator",
            "figma",
            "communication",
            "leadership",
            "teamwork",
            "problem solving",
            "analytical",
            "project management",
            "agile",
            "scrum",
            "kanban",
            "jira",
            "confluence",
            "machine learning",
            "ai",
            "data science",
            "tensorflow",
            "pytorch",
            "c++",
            "c#",
            "php",
            "ruby",
            "go",
            "rust",
            "kotlin",
            "swift",
            "marketing",
            "sales",
            "accounting",
            "finance",
            "hr",
            "recruiting",
        }
    }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Helpers – cleaning & section slicing
    # ------------------------------------------------------------------
    @staticmethod
    def _clean_text(html: str) -> str:
        """Remove tags & normalise whitespace."""
        text = re.sub(r"<[^>]+>", "\n", html)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"\r", "", text)
        text = re.sub(r" +", " ", text)
        text = re.sub(r"\n+", "\n", text)
        return text.strip()

    @staticmethod
    def _get_section(text: str, header: str) -> str:
        """Return raw text of one section, stopping at the next header."""
        other_headers = [h for h in Regex._HEADERS if h.lower() != header.lower()]
        pattern = rf"(?im)^\s*{re.escape(header)}\b\s*(.+?)(?=^\s*(?:{'|'.join(map(re.escape, other_headers))})\b\s*$|\Z)"
        match = re.search(pattern, text, flags=re.S | re.M)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _split_lines(section: str) -> List[str]:
        """Yield candidate lines, dropping obvious body paragraphs."""
        lines: list[str] = []
        for raw in section.splitlines():
            s = raw.strip(" -•\t").strip()
            if not s or len(s) < 3 or len(s) > 100:
                continue
            lines.append(s)
        return lines

    # ------------------------------------------------------------------
    # Extractors
    # ------------------------------------------------------------------
    @staticmethod
    def _extract_experience(text: str) -> List[str]:
        section = Regex._get_section(text, "experience")
        if not section:
            return []
        cleaned = []
        for s in Regex._split_lines(section):
            if re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^\n]*\d{4}", s, re.I):
                cleaned.append(s)
            elif re.search(r"\b(manager|director|analyst|engineer|developer|specialist|coordinator|assistant|administrator|consultant|executive|supervisor|lead|senior|junior)\b", s, re.I):
                if not re.search(r"\b(responsible|duties|tasks|including|such as|experience in|knowledge of)\b", s, re.I):
                    cleaned.append(s)
        return cleaned

    @staticmethod
    def _extract_education(text: str) -> List[str]:
        section = Regex._get_section(text, "education")
        if not section:
            return []
        results = []
        for s in Regex._split_lines(section):
            if len(s) > 100:
                continue
            if re.search(r"\b(bachelor|master|phd|doctorate|diploma|certificate|degree|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?|b\.?sc\.?|m\.?sc\.?)\b", s, re.I):
                results.append(s)
            elif re.search(r"\b(university|college|institute|school|academy)\b", s, re.I):
                results.append(s)
            elif re.search(r"\b(graduated|class of|\d{4})\b", s, re.I) and len(s) <= 60:
                results.append(s)
        return results

    @staticmethod
    def _extract_skills(text: str) -> List[str]:
        section = Regex._get_section(text, "skills")
        if not section:
            return []
        tokens = re.split(r"[;,/\n•&\-]", section.lower())
        skills: list[str] = []
        for tok in tokens:
            skill = tok.strip(" .-")
            if not skill or len(skill) < 3:
                continue
            if skill in Regex._ALLOWED_SKILLS:
                skills.append(skill.title())
            else:
                # partial containment check (e.g., "excel vlookup" → "excel")
                best = max(
                    [s for s in Regex._ALLOWED_SKILLS if skill in s or s in skill],
                    key=len,
                    default=None,
                )
                if best:
                    skills.append(best.title())
        # dedupe while preserving order
        return list(dict.fromkeys(skills))

    @staticmethod
    def _extract_highlights(text: str) -> List[str]:
        return Regex._split_lines(Regex._get_section(text, "highlights"))

    @staticmethod
    def _extract_main_summary(text: str) -> Optional[str]:
        section = Regex._get_section(text, "summary")
        lines = Regex._split_lines(section)
        return " ".join(lines) if lines else None

    @staticmethod
    def _extract_languages(text: str) -> List[str]:
        """Return compact language names like 'English', 'Spanish'."""
        langs = [
            l.title()
            for l in Regex._split_lines(Regex._get_section(text, "languages"))
            if len(l.split()) <= 2 and len(l) <= 20
        ]
        return langs

    @staticmethod
    def _extract_certification(text: str) -> List[str]:
        """Return any certification lines."""
        return Regex._split_lines(Regex._get_section(text, "certification"))