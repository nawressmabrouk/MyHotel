import tkinter as tk
from tkinter import ttk, messagebox
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
    def show_stats(self):
        # Taux d'occupation sur le mois en cours
        query_occup = """
            SELECT COUNT(DISTINCT chambre_id) as occupees
            FROM reservations
            WHERE statut='active' AND date_arrivee <= CURDATE() AND date_depart >= CURDATE()
        """
        occupees = db.execute_query(query_occup, fetch_one=True)['occupees'] or 0
        total_chambres = db.execute_query("SELECT COUNT(*) as total FROM chambres", fetch_one=True)['total']
        taux = (occupees / total_chambres * 100) if total_chambres else 0

        # Chiffre d'affaires total (factures payées)
        ca = db.execute_query("SELECT SUM(montant_total) as total FROM factures", fetch_one=True)['total'] or 0

        messagebox.showinfo("Statistiques",
            f"Taux d'occupation actuel : {taux:.1f}%\n"
            f"Chiffre d'affaires total : {ca:.2f} €")