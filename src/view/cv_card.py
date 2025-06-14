import customtkinter as ctk
from src.model.search_result import SearchResult

class CvCard(ctk.CTkFrame):
    def __init__(self, parent, search_result: SearchResult, **kwargs):
        super().__init__(parent, height=250, **kwargs)

        self.configure(corner_radius=10, border_width=1, border_color="#444")

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=10, pady=10)

        full_name = search_result.applicant_profile.first_name + " " + search_result.applicant_profile.last_name
        self.name_label = ctk.CTkLabel(self.content, text=full_name)
        self.name_label.pack()