import customtkinter as ctk
from src.model.search_result import SearchResult
from tkinter import Toplevel
from tkhtmlview import HTMLLabel

class CvCard(ctk.CTkFrame):
    def __init__(self, parent, search_result: SearchResult, **kwargs):
        super().__init__(parent, height=250, **kwargs)

        self.configure(corner_radius=10, border_width=1, border_color="#444", fg_color="#2a2a2a")

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=10, pady=10)
        self.search_result = search_result

        header_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        header_frame.pack(fill="x")

        full_name = search_result.applicant_profile.full_name()
        name_label = ctk.CTkLabel(header_frame, text=full_name, font=("Arial", 14, "bold"))
        name_label.pack(side="left")

        total_matches = sum(search_result.matches.values())
        match_label = ctk.CTkLabel(
            header_frame,
            text=f"{total_matches} match{'es' if total_matches != 1 else ''}",
            font=("Arial", 10),
            text_color="#AAAAAA"
        )
        match_label.pack(side="right", expand=True, anchor='e')

        subtitle = ctk.CTkLabel(self.content, text="Matched keywords:", font=("Arial", 14))
        subtitle.pack(anchor="w", pady=(5, 2))

        match_frame = ctk.CTkScrollableFrame(self.content, height=60, fg_color="transparent")
        match_frame.pack()

        for i, (keyword, count) in enumerate(search_result.matches.items(), start=1):
            label = ctk.CTkLabel(
                match_frame,
                text=f"{i}. {keyword}: {count} occurrence{'s' if count != 1 else ''}",
                font=("Arial", 13),
                anchor="w"
            )
            label.pack(anchor="w")

        button_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        summary_button = ctk.CTkButton(button_frame, text="Summary", width=100,
            command=self.show_summary_popup)
        summary_button.pack(side="left", expand=True, padx=(0, 5))

        view_cv_button = ctk.CTkButton(button_frame, text="View CV", width=100,
            command=lambda: self.show_pdf_html(search_result.pdf.cv_raw))
        view_cv_button.pack(side="right", expand=True, padx=(5, 0))

    def show_pdf_html(self, html_str: str):
        top = Toplevel(self.winfo_toplevel())
        top.title("View CV (HTML)")
        top.geometry("800x600")

        label = HTMLLabel(top, html=html_str, background="white", foreground="black")
        label.pack(fill="both", expand=True, padx=10, pady=10)

    def show_summary_popup(self):
        top = Toplevel(self.winfo_toplevel())
        top.title("CV Summary")
        top.geometry("700x600")

        # Outer padding frame for aesthetic spacing
        outer_frame = ctk.CTkFrame(top, fg_color="transparent")
        outer_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollable content
        scrollable = ctk.CTkScrollableFrame(outer_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True)

        profile = self.search_result.applicant_profile
        summary_obj = self.search_result.summary

        # Helper to create a bordered section
        def add_section_frame(title):
            section_frame = ctk.CTkFrame(scrollable, fg_color="#333333", corner_radius=10)
            section_frame.pack(fill="x", expand=True, pady=10, padx=5)
            ctk.CTkLabel(section_frame, text=title, font=("Arial", 14, "bold")).pack(anchor="w", pady=(5, 2), padx=10)
            return section_frame

        # Applicant Info Section
        profile_frame = add_section_frame("Applicant Information")
        info_lines = [
            f"Name: {profile.full_name()}",
            f"Date of Birth: {profile.date_of_birth or '-'}",
            f"Address: {profile.address or '-'}",
            f"Phone Number: {profile.phone_number or '-'}"
        ]
        for line in info_lines:
            ctk.CTkLabel(profile_frame, text=line, font=("Arial", 13), anchor="w", justify="left").pack(anchor="w", padx=15, pady=2)

        # List-type section
        def add_list_section(title, items):
            if items:
                frame = add_section_frame(title)
                for item in items:
                    ctk.CTkLabel(frame, text=f"• {item}", font=("Arial", 13), wraplength=650, justify="left").pack(anchor="w", padx=15, pady=2)

        # Text-only section
        def add_text_section(title, text):
            if text:
                frame = add_section_frame(title)
                ctk.CTkLabel(frame, text=text, font=("Arial", 13), wraplength=650, justify="left").pack(anchor="w", padx=15, pady=5)

        # Summary content
        add_list_section("Experience", summary_obj.experience)
        add_list_section("Education", summary_obj.education)
        add_list_section("Skills", summary_obj.skills)
        add_list_section("Highlights", summary_obj.highlights)
        add_text_section("Summary", summary_obj.summary)
        add_list_section("Languages", summary_obj.languages)
        add_list_section("Certifications", summary_obj.certification)



        
