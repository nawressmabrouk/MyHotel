import tkinter as tk
from tkinter import ttk
from gui.chambres import ChambresFrame
from gui.clients import ClientsFrame
from gui.reservations import ReservationsFrame
from gui.factures import FacturesFrame

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion d'Hôtel")
        self.geometry("1100x650")
        self.minsize(900, 500)

        # Notebook (onglets)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Onglets
        self.chambres_frame = ChambresFrame(self.notebook)
        self.clients_frame = ClientsFrame(self.notebook)
        self.reservations_frame = ReservationsFrame(self.notebook)
        self.factures_frame = FacturesFrame(self.notebook)

        self.notebook.add(self.chambres_frame, text="Chambres")
        self.notebook.add(self.clients_frame, text="Clients")
        self.notebook.add(self.reservations_frame, text="Réservations")
        self.notebook.add(self.factures_frame, text="Factures")
        