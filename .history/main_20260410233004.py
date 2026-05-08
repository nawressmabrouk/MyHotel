import customtkinter as ctk
from login_view import LoginView
from gui.main_window import MainWindow

def start_main_app(admin_info=None):
    """Lance l'application principale après login réussi"""
    app = MainWindow(admin_info=admin_info)
    app.mainloop()

if __name__ == "__main__":
    # Configuration du thème
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    '''# Afficher la fenêtre de connexion
    login_window = LoginView(on_success=start_main_app)
    login_window.mainloop()'''