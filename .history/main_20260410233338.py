import customtkinter as ctk
from gui.main_window import MainWindow

def start_main_app():
    """Lance l'application principale"""
    app = MainWindow()  # Pas d'admin_info pour l'instant
    app.mainloop()

if __name__ == "__main__":
    # Configuration du thème
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    start_main_app()