import customtkinter as ctk
from gui.chambres import ChambresFrame
from gui.clients import ClientsFrame
from gui.dashboard import DashboardFrame
from gui.factures import FacturesFrame
from gui.home import HomeFrame
from gui.reservations import ReservationsFrame
from gui.login_dialog import LoginDialog

# Configuration du thème
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.admin_info = None
        self.is_logged_in = False
        
        self.title("Gestion d'Hôtel - MyHotel PMS")
        self.geometry("1300x750")
        self.minsize(1000, 600)

        # Configuration de la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ========== NAVIGATION MODERNE ==========
        self.nav_frame = ctk.CTkFrame(
            self, 
            height=70, 
            corner_radius=0,
            fg_color="#1a1a2e",
            border_width=0
        )
        self.nav_frame.grid(row=0, column=0, sticky="ew")
        self.nav_frame.grid_propagate(False)

        # Logo / Titre dans la navbar
        self.logo_label = ctk.CTkLabel(
            self.nav_frame,
            text="🏨 MyHotel PMS",
            font=("Arial", 22, "bold"),
            text_color="#e67e22"
        )
        self.logo_label.pack(side="left", padx=(30, 0), pady=15)

        # Frame pour les boutons de navigation
        self.buttons_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.buttons_frame.pack(side="left", padx=(50, 0), pady=10)

        # Configuration des boutons de navigation
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

        # Activer le premier bouton
        self.set_active_button("Accueil")

        # ========== ICÔNE DE LOGIN (en haut à droite) ==========
        self.login_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.login_frame.pack(side="right", padx=(0, 30), pady=15)

        # Icône de login (cliquable)
        self.login_icon = ctk.CTkLabel(
            self.login_frame,
            text="🔐",
            font=("Arial", 24),
            text_color="white",
            cursor="hand2"
        )
        self.login_icon.pack(side="right", padx=10)
        self.login_icon.bind("<Button-1>", lambda e: self.show_login_dialog())

        # Label pour afficher le nom de l'admin connecté
        self.admin_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            font=("Arial", 12),
            text_color="white"
        )
        self.admin_label.pack(side="right", padx=10)

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
        
        # Désactiver les boutons de navigation au départ (sauf Accueil)
        self.set_navigation_enabled(False)
        
        # Afficher le dialogue de login au démarrage
        self.after(100, self.show_login_dialog)

    def show_login_dialog(self):
        """Affiche le dialogue de connexion"""
        dialog = LoginDialog(self, self.on_login_success)
        dialog.focus()

    def on_login_success(self, admin_info):
        """Appelé après une connexion réussie"""
        self.admin_info = admin_info
        self.is_logged_in = True
        
        # Mettre à jour l'affichage de l'admin
        self.admin_label.configure(text=f"👤 {admin_info['username']}")
        
        # Changer l'icône de login en icône de déconnexion
        self.login_icon.configure(text="🔓", cursor="hand2")
        self.login_icon.unbind("<Button-1>")
        self.login_icon.bind("<Button-1>", lambda e: self.logout())
        
        # Activer tous les boutons de navigation
        self.set_navigation_enabled(True)
        
        # Activer les cartes cliquables sur la page d'accueil
        if "Accueil" in self.frames:
            self.frames["Accueil"].set_cards_enabled(True)
        
        # Message de bienvenue
        from tkinter import messagebox
        messagebox.showinfo("Bienvenue", f"Bienvenue {admin_info['username']} !")

    def logout(self):
        """Déconnexion"""
        from tkinter import messagebox
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.admin_info = None
            self.is_logged_in = False
            
            # Réinitialiser l'affichage
            self.admin_label.configure(text="")
            self.login_icon.configure(text="🔐", cursor="hand2")
            self.login_icon.unbind("<Button-1>")
            self.login_icon.bind("<Button-1>", lambda e: self.show_login_dialog())
            
            # Désactiver les boutons de navigation
            self.set_navigation_enabled(False)
            
            # Désactiver les cartes sur la page d'accueil
            if "Accueil" in self.frames:
                self.frames["Accueil"].set_cards_enabled(False)
            
            # Retourner à l'accueil
            self.switch_to_tab("Accueil")
            
            messagebox.showinfo("Déconnexion", "Vous avez été déconnecté.")

    def set_navigation_enabled(self, enabled):
        """Active ou désactive les boutons de navigation"""
        state = "normal" if enabled else "disabled"
        for tab_name, btn in self.nav_buttons.items():
            if tab_name != "Accueil":  # L'accueil reste accessible même sans login
                btn.configure(state=state)
        
        # Désactiver visuellement les boutons désactivés
        if not enabled:
            for tab_name, btn in self.nav_buttons.items():
                if tab_name != "Accueil":
                    btn.configure(fg_color="gray", hover_color="gray")

    def set_active_button(self, tab_name):
        for name, btn in self.nav_buttons.items():
            if name == tab_name:
                btn.configure(
                    fg_color="#e67e22",
                    text_color="white"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="white"
                )

    def show_frame(self, page_name):
        if page_name in self.frames:
            self.frames[page_name].tkraise()

    def switch_to_tab(self, tab_name):
        self.current_tab = tab_name
        self.set_active_button(tab_name)
        self.show_frame(tab_name)