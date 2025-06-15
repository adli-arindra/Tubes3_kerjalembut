import customtkinter as ctk
from tkinter import ttk
from src.view.cv_card import CvCard
from src.model.search_result import SearchResult
from src.model.applicant_profile import ApplicantProfile
from src.model.application_detail import ApplicationDetail
from src.utils.sql import ApplicantDatabase
from src.utils.pattern_matching import PatternMatching
import concurrent.futures
import os
import time

class Homepage:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.root.title("CV Analyzer App")
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        self.db = ApplicantDatabase()
        self.search_results: list[SearchResult] = []
        self.algorithm_var = ctk.StringVar(value="KMP")
        self.keyword_var = ctk.StringVar(value="")
        self.cv_cards = []
        self.fuzzy_enabled = ctk.BooleanVar(value=True)
        self.match_count = ctk.IntVar(value=10)
        self.prefetched_data = []
        self.prefetch()

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

        self.fuzzy_checkbox = ctk.CTkCheckBox(
            self.container,
            text="Enable Fuzzy Matching",
            variable=self.fuzzy_enabled
        )
        self.fuzzy_checkbox.pack(anchor='w', pady=10)

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

        self.status_label = ctk.CTkLabel(self.container, text="", font=("Arial", 14), text_color="#AAAAAA")
        self.status_label.pack(pady=(5, 0), anchor='w')

        self.results_frame = ctk.CTkScrollableFrame(self.container)
        self.results_frame.pack(fill="both", expand=True, pady=(10, 0))

        for i in range(3):
            self.results_frame.grid_columnconfigure(i, weight=1)

    def validate_entry_matches(self, value):
        if value == "":
            return True 
        return value.isdigit() and int(value) > 0
    
    def prefetch(self):
        self.prefetched_data = []
        detail_ids = self.db.get_all_detail_ids()

        for detail_id in detail_ids:
            try:
                result = self.db.get_application_with_details(detail_id)
                if not result:
                    continue

                applicant, application_detail = result
                application_pdf = self.db.get_application_pdf(application_detail.detail_id)

                if not application_pdf or not application_pdf.cv_text:
                    continue

                self.prefetched_data.append((applicant, application_detail, application_pdf))

            except Exception:
                import traceback; traceback.print_exc()

    def _on_search(self):
        try:
            self.clear_cv_cards()
            keywords = list(dict.fromkeys([kw.strip() for kw in self.keyword_var.get().lower().split(',') if kw.strip()]))
            match_limit = self.match_count.get()
            max_workers = min(32, os.cpu_count() * 5)

            def process_entry(entry):
                try:
                    applicant, application_details, application_pdf = entry
                    cv_text = application_pdf.cv_text
                    matches = {}
                    algorithm = self.algorithm_var.get()

                    if algorithm == "Aho-Corasick":
                        match_score, matches = PatternMatching.aho_corasick(cv_text, keywords)
                    else:
                        for keyword in keywords:
                            count = 0
                            if algorithm == "KMP":
                                count = PatternMatching.kmp(cv_text, keyword)
                            elif algorithm == "Boyer-Moore":
                                count = PatternMatching.bm(cv_text, keyword)
                            if count > 0:
                                matches[keyword] = count
                        match_score = sum(matches.values())

                    result = None
                    if matches:
                        result = (match_score, SearchResult(applicant, application_details, application_pdf, matches))

                    fuzzy_result = None

                    if self.fuzzy_enabled.get():
                        fuzzy_score = 0
                        fuzzy_valid = True
                        fuzzy_distances = {}

                        for keyword in keywords:
                            if keyword in matches:
                                continue
                            dist = PatternMatching.min_ld(cv_text, keyword, 1)
                            if dist is None or dist > 10:
                                fuzzy_valid = False
                                break
                            fuzzy_distances[keyword] = dist
                            fuzzy_score += dist

                        if fuzzy_valid:
                            fuzzy_result = (fuzzy_score, SearchResult(applicant, application_details, application_pdf, fuzzy_distances))

                    return result, fuzzy_result

                except Exception:
                    import traceback; traceback.print_exc()
                    return None, None


            def on_complete(results_with_scores, duration):
                try:
                    exact_matches = []
                    fuzzy_candidates = []

                    for exact, fuzzy in results_with_scores:
                        if exact:
                            exact_matches.append(exact)
                        elif fuzzy:
                            fuzzy_candidates.append(fuzzy)

                    exact_matches.sort(key=lambda x: x[0], reverse=True)
                    fuzzy_candidates.sort(key=lambda x: x[0])

                    final_results = exact_matches[:match_limit]
                    remaining = match_limit - len(final_results)
                    if remaining > 0:
                        final_results += fuzzy_candidates[:remaining]

                    self.search_results = [res for _, res in final_results]
                    for res in self.search_results:
                        self.add_cv_card(res)

                    ms = duration * 1000
                    self.status_label.configure(
                        text=f"Scanned {len(self.prefetched_data)} CVs in {ms:.0f} ms."
                    )
                except Exception:
                    import traceback; traceback.print_exc()

            def run_in_background():
                start_time = time.time()
                results = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = [executor.submit(process_entry, entry) for entry in self.prefetched_data]
                    for f in concurrent.futures.as_completed(futures):
                        res = f.result()
                        if res:
                            results.append(res)
                duration = time.time() - start_time
                self.root.after(0, lambda: on_complete(results, duration))

            import threading
            threading.Thread(target=run_in_background, daemon=True).start()

        except Exception as e:
            print(f"Error during search: {e}")


    def fuzzy_search(text: str, pattern: str, max_distance=5) -> int | None:
        t_len = len(text)
        p_len = len(pattern)
        window = p_len + max_distance
        best_distance = max_distance + 1

        for i in range(t_len - p_len + 1):
            window_text = text[i:i + p_len]
            dist = PatternMatching.ld(window_text, pattern)
            if dist < best_distance:
                best_distance = dist
            if best_distance == 0:
                break

        return best_distance if best_distance <= max_distance else None

    def clear_cv_cards(self):
        for card in self.cv_cards:
            card.destroy()
        self.cv_cards.clear()

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
