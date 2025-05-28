# Card.py
import customtkinter as ctk

class CVCard(ctk.CTkFrame):
    def __init__(self, parent, name: str, matches: int, keywords: list):
        super().__init__(parent, width=200, height=180, corner_radius=10, 
                         border_width=1, border_color="#ddd")
        self.pack(side='left', padx=10, pady=10)
        self.pack_propagate(False) # Prevents the frame from shrinking to fit content

        self.name = name
        self.matches = matches
        self.keywords = keywords

        self._create_widgets()

    def _create_widgets(self):
        # 1. Top frame for name and matches
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill='x', padx=5, pady=5)
        
        name_lbl = ctk.CTkLabel(top, text=self.name, font=('Arial', 12, 'bold'))
        name_lbl.pack(side='left', padx=5)
        
        match_lbl = ctk.CTkLabel(top, text=f"{self.matches} matches", font=('Arial', 10))
        match_lbl.pack(side='right', padx=5)

        # 2. Matched keywords section label
        kw_label = ctk.CTkLabel(self, text="Matched keywords:", font=('Arial', 11, 'bold'))
        kw_label.pack(anchor='w', padx=5, pady=(5,0))

        # 3. Buttons frame (packed to bottom FIRST)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill='x', pady=5, padx=5, side='bottom') 

        summary_btn = ctk.CTkButton(btn_frame, text="Summary", width=80, height=24, 
            font=('Arial', 10))
        summary_btn.pack(side='left', padx=5)

        view_btn = ctk.CTkButton(btn_frame, text="View CV", width=80, height=24, 
                                 font=('Arial', 10))
        view_btn.pack(side='right', padx=5)

        # 4. Scrollable frame for keywords:
        # Calculate a height for the scrollable frame.
        # This will be the total card height (180) minus the estimated height of other elements.
        # Estimate: top frame (~35px) + kw_label (~25px) + btn_frame (~40px) + various paddings (~10-20px) = ~110px.
        # So, 180 - 110 = 70px remaining for the scrollable frame.
        # Adjust '70' if more/fewer lines are desired before scrolling begins,
        # or if actual component heights differ slightly.
        scrollable_frame_height = 70 # Approximately 3-4 lines of keywords

        self.keyword_scroll_frame = ctk.CTkScrollableFrame(self, 
                                                           fg_color="transparent",
                                                           height=scrollable_frame_height) # Explicit height
        # With explicit height, fill='x' and expand=False are more appropriate.
        self.keyword_scroll_frame.pack(fill='x', expand=False, padx=5, pady=(0, 5)) 

        for idx, kw in enumerate(self.keywords, 1):
            kw_text = f"{idx}. {kw['keyword']}: {kw['count']} occurrence{'s' if kw['count']>1 else ''}"
            kw_lbl = ctk.CTkLabel(self.keyword_scroll_frame, text=kw_text, font=('Arial', 10), anchor='w')
            kw_lbl.pack(fill='x', padx=5)

# Example usage (for testing Card.py independently if needed)
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("CV Card Test")
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # Sample keywords to test scrolling (should overflow)
    long_keywords_list = [
        {"keyword": "Python", "count": 1},
        {"keyword": "SQL", "count": 2},
        {"keyword": "JavaScript", "count": 3},
        {"keyword": "React", "count": 1},
        {"keyword": "Node.js", "count": 2},
        {"keyword": "MongoDB", "count": 1},
        {"keyword": "AWS", "count": 2},
        {"keyword": "Docker", "count": 1},
        {"keyword": "Kubernetes", "count": 1},
        {"keyword": "Git", "count": 3},
        {"keyword": "Agile", "count": 2},
        {"keyword": "Flask", "count": 1},
        {"keyword": "Django", "count": 2}
    ]

    # Sample keywords that should NOT overflow (should hide scrollbar)
    short_keywords_list = [
        {"keyword": "HTML", "count": 1},
        {"keyword": "CSS", "count": 2}
    ]

    card1 = CVCard(root, "Test User 1 (Long)", 7, long_keywords_list)
    card2 = CVCard(root, "Test User 2 (Short)", 3, short_keywords_list)
    card3 = CVCard(root, "Test User 3 (No Keywords)", 0, [])
    
    root.mainloop()