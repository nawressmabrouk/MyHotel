import customtkinter as ctk
from login_view import LoginView
from gui.main_window import MainWindow

def start_main_app(admin_info):
    """Lance l'application principale après login réussi"""
    app = MainWindow(admin_info=admin_info)
    app.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Créer directement la fenêtre de login
    login_window = LoginView(on_success=start_main_app)
    login_window.mainloop()