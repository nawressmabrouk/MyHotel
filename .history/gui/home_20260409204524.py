from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

import database as db


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_stats()

    def create_widgets(self):
        # Titre
        title_label = ctk.CTkLabel(self, text="Tableau de bord - Gestion Hôtel", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # Frame pour les cartes (grid 2x2)
        self.cards_frame = ctk.CTkFrame(self)
        self.cards_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # On va créer 6 cartes, donc 3 lignes de 2
        self.stats_vars = {}

        # Carte 1 : Chambres totales
        self.create_card(0, 0, "🏨 Chambres totales", "0")
        # Carte 2 : Chambres libres
        self.create_card(0, 1, "✅ Chambres libres", "0")
        # Carte 3 : Réservations actives
        self.create_card(1, 0, "📅 Réservations actives", "0")
        # Carte 4 : Clients inscrits
        self.create_card(1, 1, "👥 Clients", "0")
        # Carte 5 : Chiffre d'affaires total
        self.create_card(2, 0, "💰 Chiffre d'affaires", "0 €")
        # Carte 6 : Dernière mise à jour
        self.create_card(2, 1, "🕒 Dernière mise à jour", "")

        # Bouton actualiser
        refresh_btn = ctk.CTkButton(self, text="Actualiser", command=self.load_stats, width=200)
        refresh_btn.pack(pady=20)

    def create_card(self, row, col, title, initial_value):
        card = ctk.CTkFrame(self.cards_frame, corner_radius=10, border_width=2, border_color="gray70")
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        self.cards_frame.grid_rowconfigure(row, weight=1)
        self.cards_frame.grid_columnconfigure(col, weight=1)

        label_title = ctk.CTkLabel(card, text=title, font=("Arial", 16, "bold"))
        label_title.pack(pady=(20, 10))

        label_value = ctk.CTkLabel(card, text=initial_value, font=("Arial", 28, "bold"), text_color="blue")
        label_value.pack(pady=(0, 20))

        self.stats_vars[title] = label_value

    def load_stats(self):
        # Récupérer les données depuis la base
        # Nombre total de chambres
        total_chambres = db.execute_query("SELECT COUNT(*) as total FROM chambres", fetch_one=True)
        total_chambres = total_chambres['total'] if total_chambres else 0
        self.stats_vars["🏨 Chambres totales"].configure(text=str(total_chambres))

        # Chambres libres
        libres = db.execute_query("SELECT COUNT(*) as total FROM chambres WHERE statut = 'libre'", fetch_one=True)
        libres = libres['total'] if libres else 0
        self.stats_vars["✅ Chambres libres"].configure(text=str(libres))

        # Réservations actives
        actives = db.execute_query("SELECT COUNT(*) as total FROM reservations WHERE statut = 'active' AND date_depart >= CURDATE()", fetch_one=True)
        actives = actives['total'] if actives else 0
        self.stats_vars["📅 Réservations actives"].configure(text=str(actives))

        # Nombre de clients
        clients = db.execute_query("SELECT COUNT(*) as total FROM clients", fetch_one=True)
        clients = clients['total'] if clients else 0
        self.stats_vars["👥 Clients"].configure(text=str(clients))

        # Chiffre d'affaires total
        ca = db.execute_query("SELECT SUM(montant_total) as total FROM factures", fetch_one=True)
        ca = ca['total'] if ca and ca['total'] else 0
        self.stats_vars["💰 Chiffre d'affaires"].configure(text=f"{ca:.2f} €")

        # Dernière mise à jour
        now = datetime.now().strftime("%H:%M:%S")
        self.stats_vars["🕒 Dernière mise à jour"].configure(text=now)