import customtkinter as ctk

from gui.chambres import ChambresFrame
from gui.clients import ClientsFrame
from gui.dashboard import DashboardFrame
from gui.factures import FacturesFrame
from gui.home import HomeFrame
from gui.reservations import ReservationsFrame


class MainWindow(ctk.CTkFrame):
    def __init__(self, parent, admin_info=None):
        super().__init__(parent)
        self.parent = parent
        self.admin_info = admin_info
        
        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True)
        
        parent.title("Gestion d'Hôtel - MyHotel")
        parent.geometry("1300x750")
        parent.minsize(1000, 600)

        # Configuration de la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ========== NAVIGATION ==========
        self.nav_frame = ctk.CTkFrame(
            self, 
            height=70, 
            corner_radius=0,
            fg_color="#1a1a2e",
            border_width=0
        )
        self.nav_frame.grid(row=0, column=0, sticky="ew")
        self.nav_frame.grid_propagate(False)

        # Logo
        self.logo_label = ctk.CTkLabel(
            self.nav_frame,
            text="🏨 MyHotel",
            font=("Arial", 22, "bold"),
            text_color="#e67e22"
        )
        self.logo_label.pack(side="left", padx=(30, 0), pady=15)

        # Boutons de navigation
        self.buttons_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.buttons_frame.pack(side="left", padx=(50, 0), pady=10)

        nav_items = [
            ("🏠 Accueil", "Accueil"),
            ("📊 Dashboard", "Dashboard"),
            ("🛏️ Chambres", "Chambres"),
            ("👥 Clients", "Clients"),
            ("📅 Réservations", "Réservations"),
            ("💰 Factures", "Factures")
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
                text_color="white",
                hover_color="#e67e22",
                command=lambda t=tab_name: self.switch_to_tab(t)
            )
            btn.pack(side="left", padx=5, pady=5)
            self.nav_buttons[tab_name] = btn

        self.set_active_button("Accueil")

        # Info admin connecté
        if self.admin_info:
            self.admin_label = ctk.CTkLabel(
                self.nav_frame,
                text=f"👤 {self.admin_info['username']}",
                font=("Arial", 12),
                text_color="white"
            )
            self.admin_label.pack(side="right", padx=30)

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

        # Placement des frames
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # Afficher l'accueil par défaut
        self.show_frame("Accueil")
        
        # Activer les cartes
        if "Accueil" in self.frames:
            self.frames["Accueil"].set_cards_enabled(True)

    def set_active_button(self, tab_name):
        for name, btn in self.nav_buttons.items():
            if name == tab_name:
                btn.configure(fg_color="#e67e22", text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color="white")

    def show_frame(self, page_name):
        if page_name in self.frames:
            self.frames[page_name].tkraise()

    def switch_to_tab(self, tab_name):
        self.current_tab = tab_name
        self.set_active_button(tab_name)
        self.show_frame(tab_name)