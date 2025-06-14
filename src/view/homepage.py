import customtkinter as ctk
from tkinter import ttk
from src.view.cv_card import CvCard
from src.model.search_result import SearchResult
from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
from src.utils.sql import ApplicantDatabase
from src.utils.pdf_reader import PDFReader
from src.utils.pattern_matching import PatternMatching

class Homepage:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.root.title("CV Analyzer App")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.db = ApplicantDatabase()
        self.search_results: list[SearchResult] = []
        self.algorithm_var = ctk.StringVar(value="KMP")
        self.keyword_var = ctk.StringVar(value="")
        self.cv_cards = []
        self.match_count = ctk.IntVar(value=10)

        self.container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=(5,20))

        self.label = ctk.CTkLabel(self.container, text="Keywords:", font=("Arial", 18))
        self.label.pack(anchor='w')

        self.entry_keyword = ctk.CTkEntry(self.container, placeholder_text="Python, React, HTML", height=30, textvariable=self.keyword_var)
        self.entry_keyword.pack(anchor="w", pady=5, fill='x')

        self.label = ctk.CTkLabel(
            self.container,
            text="Hint: Enter multiple keywords with a ',' (comma) as a separator between each keyword (if multiple keywords are provided)",
            font=("Arial", 14),
            text_color="#FF7F7F",
            wraplength=400
        )
        self.label.pack(fill="x")

        self.label = ctk.CTkLabel(self.container, text="Search Algorithm:", font=("Arial", 18))
        self.label.pack(anchor='w')

        self.radio_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.radio_frame.pack(fill="x", pady=10, padx=(75, 0))

        self.kmp_radio = ctk.CTkRadioButton(self.radio_frame, text="KMP", variable=self.algorithm_var, value="KMP")
        self.bm_radio = ctk.CTkRadioButton(self.radio_frame, text="Boyer-Moore", variable=self.algorithm_var, value="Boyer-Moore")
        self.aho_radio = ctk.CTkRadioButton(self.radio_frame, text="Aho-Corasick", variable=self.algorithm_var, value="Aho-Corasick")

        self.kmp_radio.pack(side="left", expand=True, fill="x", padx=5)
        self.bm_radio.pack(side="left", expand=True, fill="x", padx=5)
        self.aho_radio.pack(side="left", expand=True, fill="x", padx=5)

        self.label = ctk.CTkLabel(self.container, text="Show Matches:", font=("Arial", 18))
        self.label.pack(anchor='w')

        vcmd = self.root.register(self.validate_entry_matches)

        self.entry_matches = ctk.CTkEntry(
            self.container,
            placeholder_text="10",
            height=30,
            width=150,
            validate="key",
            validatecommand=(vcmd, "%P"),
            textvariable=self.match_count
        )
        self.entry_matches.pack(anchor="w", pady=5, padx=0)

        self.search_button = ctk.CTkButton(self.container, text="Search", command=self._on_search)
        self.search_button.pack(fill="x", padx=10, pady=(10, 0))

        self.results_frame = ctk.CTkScrollableFrame(self.container)
        self.results_frame.pack(fill="both", expand=True, pady=(10, 0))

        for i in range(3):
            self.results_frame.grid_columnconfigure(i, weight=1)

    def validate_entry_matches(self, value):
        if value == "":
            return True 
        return value.isdigit() and int(value) > 0
    
    def _on_search(self):
        try:
            keywords = list(dict.fromkeys([kw.strip() for kw in self.keyword_var.get().split(',') if kw.strip()]))
            application_count = self.db.get_application_count()
            results_with_scores = []

            for detail_id in range(1, application_count + 1):
                result: tuple[ApplicantProfile, ApplicationDetail] = self.db.get_application_with_details(detail_id)
                (applicant, application_details) = result
                cv_text = application_details.cv_text

                matches: dict[str, int] = {}

                if self.algorithm_var == "Aho-Corasick":
                    match_score, matches = PatternMatching.aho_corasick(cv_text, keywords)
                else:
                    for keyword in keywords:
                        match self.algorithm_var:
                            case "KMP":
                                count = PatternMatching.kmp_count(cv_text, keyword)
                            case "Boyer-Moore":
                                count = PatternMatching.bm_count(cv_text, keyword)
                            case _:
                                count = 0

                        if count > 0:
                            matches[keyword] = count

                    match_score = sum(matches.values())

                if matches:
                    results_with_scores.append((
                        match_score,
                        SearchResult(applicant, application_details, matches)
                    ))

            results_with_scores.sort(key=lambda x: x[0], reverse=True)
            self.search_results = [res for _, res in results_with_scores[:self.match_count]]

            for search_result in self.search_results:
                self.add_cv_card(search_result)

        except Exception as e:
            print(f"Error during search: {e}")

    def add_cv_card(self, search_result: SearchResult):
        card = CvCard(self.results_frame, search_result=search_result)
        
        index = len(self.cv_cards)
        row = index // 3
        col = index % 3

        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        self.cv_cards.append(card)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    app = Homepage(root)
    app.run()
