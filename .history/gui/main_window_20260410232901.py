import customtkinter as ctk

from gui.chambres import ChambresFrame
from gui.clients import ClientsFrame
from gui.dashboard import DashboardFrame
from gui.factures import FacturesFrame
from gui.home import HomeFrame
from gui.reservations import ReservationsFrame

# Configuration du thème
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__():
        super().__init__()
        #self.admin_info = admin_info
        self.title("Gestion d'Hôtel - MyHotel PMS")
        self.geometry("1300x750")
        self.minsize(1000, 600)

        # Configuration de la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ========== NAVIGATION MODERNE ==========
        # Frame supérieure pour la navigation (style navbar)
        self.nav_frame = ctk.CTkFrame(
            self, 
            height=70, 
            corner_radius=0,
            fg_color=("#e67e22", "#e67e22"),
            border_width=0
        )
        self.nav_frame.grid(row=0, column=0, sticky="ew")
        self.nav_frame.grid_propagate(False)

        # Logo / Titre dans la navbar
        self.logo_label = ctk.CTkLabel(
            self.nav_frame,
            text="🏨 MyHotel",
            font=("Arial", 20, "bold"),
            text_color=("#3a7eb6", "#3a7eb6")
        )
        self.logo_label.pack(side="left", padx=(30, 0), pady=15)

        # Frame pour les boutons de navigation (remplace le tabview)
        self.buttons_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.buttons_frame.pack(side="left", padx=(50, 0), pady=10)

        # Configuration des boutons de navigation
        nav_items = [
            ("Accueil", "Accueil"),
            ("Dashboard", "Dashboard"),
            ("Chambres", "Chambres"),
            ("Clients", "Clients"),
            ("Réservations", "Réservations"),
            ("Factures", "Factures")
        ]

        self.nav_buttons = {}
        self.current_tab = "Accueil"

        for text, tab_name in nav_items:
            btn = ctk.CTkButton(
                self.buttons_frame,
                text=text,
                font=("Arial", 14, "bold"),
                width=120,
                height=40,
                corner_radius=20,
                fg_color="transparent",
                text_color=("white", "white"),
                hover_color=("#3a7eb6", "#2c5a8c"),
                command=lambda t=tab_name: self.switch_to_tab(t)
            )
            btn.pack(side="left", padx=5, pady=5)
            self.nav_buttons[tab_name] = btn

        # Activer le premier bouton
        self.set_active_button("Accueil")

        # ========== CONTENU PRINCIPAL ==========
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Dictionnaire des frames
        self.frames = {}

        # Création des frames
        self.frames["Accueil"] = HomeFrame(self.content_frame, main_app=self)
        self.frames["Dashboard"] = DashboardFrame(self.content_frame)
        self.frames["Chambres"] = ChambresFrame(self.content_frame)
        self.frames["Clients"] = ClientsFrame(self.content_frame)
        self.frames["Réservations"] = ReservationsFrame(self.content_frame)
        self.frames["Factures"] = FacturesFrame(self.content_frame)

        # Placement de tous les frames dans la grille
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # Afficher le frame par défaut
        self.show_frame("Accueil")
        # Afficher le nom de l'admin en bas à droite 
        if admin_info:
            admin_label = ctk.CTkLabel(
                self.nav_frame, 
                text=f"👤 {admin_info['username']}",
                font=("Arial", 12)
            )
            admin_label.pack(side="right", padx=20)

    def set_active_button(self, tab_name):
        """Met en surbrillance le bouton actif"""
        for name, btn in self.nav_buttons.items():
            if name == tab_name:
                btn.configure(
                    fg_color=("#3a7eb6", "#2c5a8c"),
                    text_color="white"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("white", "white")
                )

    def show_frame(self, page_name):
        """Affiche le frame sélectionné"""
        if page_name in self.frames:
            self.frames[page_name].tkraise()

    def switch_to_tab(self, tab_name):
        """Change d'onglet et met à jour l'interface"""
        self.current_tab = tab_name
        self.set_active_button(tab_name)
        self.show_frame(tab_name)
    
 
 
 

 
 
 

 
 