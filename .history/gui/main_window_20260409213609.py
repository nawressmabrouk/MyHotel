import customtkinter as ctk
from gui.home import HomeFrame
from gui.dashboard import DashboardFrame
from gui.chambres import ChambresFrame
from gui.clients import ClientsFrame
from gui.reservations import ReservationsFrame
from gui.factures import FacturesFrame

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion d'Hôtel")
        self.geometry("1200x700")
        self.minsize(900, 500)

        # Tabview avec style personnalisé
        self.tabview = ctk.CTkTabview(self, width=1100, height=600)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Personnalisation de la taille des onglets
        # On accède au style interne pour augmenter la police
        self.tabview._segmented_button.configure(font=("Arial", 16, "bold"))
        self.tabview._segmented_button.configure(height=45)  # hauteur des onglets

        # Ajout des onglets
        self.tabview.add("Accueil")
        self.tabview.add("Dashboard")
        self.tabview.add("Chambres")
        self.tabview.add("Clients")
        self.tabview.add("Réservations")
        self.tabview.add("Factures")

        # Frames
        self.home_frame = HomeFrame(self.tabview.tab("Accueil"), main_app=self)
        self.home_frame.pack(fill="both", expand=True)

        self.dashboard_frame = DashboardFrame(self.tabview.tab("Dashboard"))
        self.dashboard_frame.pack(fill="both", expand=True)

        self.chambres_frame = ChambresFrame(self.tabview.tab("Chambres"))
        self.chambres_frame.pack(fill="both", expand=True)

        self.clients_frame = ClientsFrame(self.tabview.tab("Clients"))
        self.clients_frame.pack(fill="both", expand=True)

        self.reservations_frame = ReservationsFrame(self.tabview.tab("Réservations"))
        self.reservations_frame.pack(fill="both", expand=True)

        self.factures_frame = FacturesFrame(self.tabview.tab("Factures"))
        self.factures_frame.pack(fill="both", expand=True)

        # Sélection par défaut
    self.home_frame = HomeFrame(self.tabview.tab("Accueil"), main_app=self)
    def switch_to_tab(self, tab_name):
        """Méthode publique pour changer d'onglet depuis n'importe quel frame"""
        self.tabview.set(tab_name)