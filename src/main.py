import customtkinter as ctk
from src.view.homepage import Homepage

if __name__ == "__main__":
    root = ctk.CTk()
    app = Homepage(root) # masih dummy
    app.run()