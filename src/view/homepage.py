# Homepage.py
import customtkinter as ctk
from tkinter import ttk
from src.view.card import CVCard # Import the new CVCard class

class Homepage:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.root.title("CV Analyzer App")
        self.root.geometry("1024x800")
        self.root.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        title = ctk.CTkLabel(self.root, text="CV Analyzer App", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        kw_label = ctk.CTkLabel(self.root, text="Keywords:", font=("Arial", 12))
        kw_label.pack(anchor='w', padx=20)
        
        self.kw_entry = ctk.CTkEntry(self.root, font=("Arial", 12), width=400, height=30)
        self.kw_entry.insert(0, "React, Express, HTML")
        self.kw_entry.configure(state='readonly')
        self.kw_entry.pack(padx=20, pady=5, fill='x')

        alg_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        alg_frame.pack(anchor='w', padx=20, pady=10)
        
        alg_label = ctk.CTkLabel(alg_frame, text="Search Algorithm:", font=("Arial", 12))
        alg_label.pack(side='left')

        self.algo_var = ctk.StringVar(value="BM")
        kmp_rb = ctk.CTkRadioButton(alg_frame, text="KMP", variable=self.algo_var, value="KMP")
        bm_rb = ctk.CTkRadioButton(alg_frame, text="BM", variable=self.algo_var, value="BM")
        kmp_rb.pack(side='left', padx=10)
        bm_rb.pack(side='left')

        top_match_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        top_match_frame.pack(anchor='w', padx=20, pady=10)
        
        top_match_label = ctk.CTkLabel(top_match_frame, text="Top Matches:", font=("Arial", 12))
        top_match_label.pack(side='left')

        self.top_match_var = ctk.StringVar(value='3')
        vcmd = (self.root.register(self.validate_positive_integer_input), '%P')
        
        self.top_match_entry = ctk.CTkEntry(
            top_match_frame, 
            font=("Arial", 12), 
            width=100, 
            height=30,
            textvariable=self.top_match_var,
            validate='key', 
            validatecommand=vcmd 
        )
        self.top_match_entry.pack(side='left', padx=10)

        self.search_btn = ctk.CTkButton(self.root, text="Search", width=400, height=40, 
            font=("Arial", 12, "bold"))
        self.search_btn.pack(pady=20)

        self.results_label = ctk.CTkLabel(self.root, text="Results\n100 CVs scanned in 100ms", 
            font=("Arial", 12, "bold"))
        self.results_label.pack(pady=10)

        self.cards_frame = ctk.CTkScrollableFrame(self.root, width=950, height=400)
        self.cards_frame.pack(padx=20, pady=5, fill='both', expand=True)

        self.add_sample_cards()
    
    def validate_positive_integer_input(self, P):
        if P == "":
            return True
        
        if P.isdigit():
            if int(P) > 0:
                return True
            else:
                return False
        else:
            return False

    # Removed the make_card method, now handled by CVCard class

    def add_sample_cards(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        # Instantiate CVCard objects directly
        CVCard(self.cards_frame, "Farhan", 4, [
            {"keyword": "React", "count": 1},
            {"keyword": "Express", "count": 2},
            {"keyword": "HTML", "count": 1}
        ])

        CVCard(self.cards_frame, "Aland", 1, [
            {"keyword": "React", "count": 1}
        ])

        CVCard(self.cards_frame, "Ariel", 1, [
            {"keyword": "Express", "count": 1}
        ])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    app = Homepage(root)
    app.run()