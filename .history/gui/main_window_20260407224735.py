import customtkinter as ctk
from gui.chambres import ChambresFrame
from gui.clients import ClientsFrame
from gui.reservations import ReservationsFrame
from gui.factures import FacturesFrame

# Configuration du thème et de l'apparence
ctk.set_appearance_mode("dark")      # "dark", "light", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion d'Hôtel - CustomTkinter")
        self.geometry("1200x700")
        self.minsize(900, 500)

        # Création d'un notebook (onglets) avec CTkTabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Ajout des onglets
        self.tabview.add("Chambres")
        self.tabview.add("Clients")
        self.tabview.add("Réservations")
        self.tabview.add("Factures")

        # Frames dans chaque onglet
        self.chambres_frame = ChambresFrame(self.tabview.tab("Chambres"))
        self.chambres_frame.pack(fill="both", expand=True)

        self.clients_frame = ClientsFrame(self.tabview.tab("Clients"))
        self.clients_frame.pack(fill="both", expand=True)

        self.reservations_frame = ReservationsFrame(self.tabview.tab("Réservations"))
        self.reservations_frame.pack(fill="both", expand=True)

        self.factures_frame = FacturesFrame(self.tabview.tab("Factures"))
        self.factures_frame.pack(fill="both", expand=True)