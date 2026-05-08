import customtkinter as ctk
import database as db
from datetime import datetime

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_stats()

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Tableau de bord - Statistiques", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Frame pour les cartes
        self.cards_frame = ctk.CTkFrame(self)
        self.cards_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.stats_vars = {}

        # Création des 6 cartes
        cards_info = [
            ("🏨 Chambres totales", 0, 0),
            ("✅ Chambres libres", 0, 1),
            ("📅 Réservations actives", 1, 0),
            ("👥 Clients inscrits", 1, 1),
            ("💰 Chiffre d'affaires", 2, 0),
            ("🕒 Dernière mise à jour", 2, 1)
        ]
        for title_text, row, col in cards_info:
            self.create_card(row, col, title_text, "0")

        # Bouton actualiser
        refresh_btn = ctk.CTkButton(self, text="Actualiser", command=self.load_stats, width=200)
        refresh_btn.pack(pady=20)

    def create_card(self, row, col, title_text, initial_value):
        card = ctk.CTkFrame(self.cards_frame, corner_radius=10, border_width=2, border_color="gray70")
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        self.cards_frame.grid_rowconfigure(row, weight=1)
        self.cards_frame.grid_columnconfigure(col, weight=1)

        label_title = ctk.CTkLabel(card, text=title_text, font=("Arial", 16, "bold")text_color="#1a1a2e")
        label_title.pack(pady=(20, 10))

        label_value = ctk.CTkLabel(card, text=initial_value, font=("Arial", 28, "bold"), text_color="#1a1a2e")
        label_value.pack(pady=(0, 20))

        self.stats_vars[title_text] = label_value

    def load_stats(self):
        # Chambres totales
        total = db.execute_query("SELECT COUNT(*) as total FROM chambres", fetch_one=True)
        total = total['total'] if total else 0
        self.stats_vars["🏨 Chambres totales"].configure(text=str(total))

        # Chambres libres
        libres = db.execute_query("SELECT COUNT(*) as total FROM chambres WHERE statut = 'libre'", fetch_one=True)
        libres = libres['total'] if libres else 0
        self.stats_vars["✅ Chambres libres"].configure(text=str(libres))

        # Réservations actives (non terminées et non annulées, avec date départ >= aujourd'hui)
        actives = db.execute_query("""
            SELECT COUNT(*) as total FROM reservations 
            WHERE statut = 'active' AND date_depart >= CURDATE()
        """, fetch_one=True)
        actives = actives['total'] if actives else 0
        self.stats_vars["📅 Réservations actives"].configure(text=str(actives))

        # Nombre de clients
        clients = db.execute_query("SELECT COUNT(*) as total FROM clients", fetch_one=True)
        clients = clients['total'] if clients else 0
        self.stats_vars["👥 Clients inscrits"].configure(text=str(clients))

        # Chiffre d'affaires (factures)
        ca = db.execute_query("SELECT SUM(montant_total) as total FROM factures", fetch_one=True)
        ca = ca['total'] if ca and ca['total'] else 0
        self.stats_vars["💰 Chiffre d'affaires"].configure(text=f"{ca:.2f} €")

        # Dernière mise à jour
        now = datetime.now().strftime("%H:%M:%S")
        self.stats_vars["🕒 Dernière mise à jour"].configure(text=now)