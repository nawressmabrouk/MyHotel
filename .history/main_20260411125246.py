import customtkinter as ctk

# Forcer l'utilisation de CTk comme racine unique
import sys

from login_view import LoginView
from gui.main_window import MainWindow

def start_main_app(admin_info):
    """Lance l'application principale après login réussi"""
    # Créer et afficher la fenêtre principale
    app = MainWindow(admin_info=admin_info)
    app.mainloop()

if __name__ == "__main__":
    # Configuration du thème
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Créer une fenêtre CTk principale (elle sera réutilisée)
    root = ctk.CTk()
    root.withdraw()  # Cacher la fenêtre principale temporairement
    
    # Créer la fenêtre de login comme fenêtre enfant
    login_window = LoginView(root, on_success=start_main_app)
    
    # Démarrer la boucle principale
    root.mainloop()