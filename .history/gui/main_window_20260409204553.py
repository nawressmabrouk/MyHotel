import customtkinter as ctk
from gui.home import HomeFrame
from gui.chambres import ChambresFrame
from gui.clients import ClientsFrame
from gui.reservations import ReservationsFrame
from gui.factures import FacturesFrame

# Configuration du thème
ctk.set_appearance_mode("dark")      # ou "light"
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion d'Hôtel - Dashboard")
        self.geometry("1200x700")
        self.minsize(900, 500)

        # Tabview (onglets)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Ajouter les onglets
        self.tabview.add("Accueil")
        self.tabview.add("Chambres")
        self.tabview.add("Clients")
        self.tabview.add("Réservations")
        self.tabview.add("Factures")

        # Créer les frames dans chaque onglet
        self.home_frame = HomeFrame(self.tabview.tab("Accueil"))
        self.home_frame.pack(fill="both", expand=True)

        self.chambres_frame = ChambresFrame(self.tabview.tab("Chambres"))
        self.chambres_frame.pack(fill="both", expand=True)

        self.clients_frame = ClientsFrame(self.tabview.tab("Clients"))
        self.clients_frame.pack(fill="both", expand=True)

        self.reservations_frame = ReservationsFrame(self.tabview.tab("Réservations"))
        self.reservations_frame.pack(fill="both", expand=True)

        self.factures_frame = FacturesFrame(self.tabview.tab("Factures"))
        self.factures_frame.pack(fill="both", expand=True)

        # Optionnel : sélectionner l'onglet Accueil au démarrage
        self.tabview.set("Accueil")