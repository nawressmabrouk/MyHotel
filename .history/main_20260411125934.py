import customtkinter as ctk
from login_view import LoginView
from gui.main_window import MainWindow

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Cacher la fenêtre principale immédiatement
        self.withdraw()
        
        # Configuration
        self.title("MyHotel")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Afficher la fenêtre de login
        self.login_window = LoginView(self, self.on_login_success)
    
    def on_login_success(self, admin_info):
        # Fermer la fenêtre de login
        if hasattr(self, 'login_window'):
            self.login_window.destroy()
        
        # Afficher la fenêtre principale
        self.deiconify()
        
        # Créer et afficher l'application principale
        self.main_app = MainWindow(self, admin_info)
        self.main_app.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()