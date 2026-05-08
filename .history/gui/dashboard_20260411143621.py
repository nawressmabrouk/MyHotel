import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import ttk

import customtkinter as ctk

from controllers.dashboard_controller import DashboardController


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = DashboardController()
        self.create_widgets()
        self.load_data()
        self.start_auto_refresh()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        # Titre principal
        title_label = ctk.CTkLabel(
            self, 
            text="📊 Tableau de Bord - Hôtel Gestion", 
            font=("Arial", 24, "bold"),
            text_color="#e67e22"
        )
        title_label.pack(pady=(20, 10))

        # Frame pour les cartes (statistiques)
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=20, pady=10)

        # Frame pour les graphiques (simulés avec CTkProgressBar et labels)
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame pour les tableaux récents
        self.tables_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tables_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ========== BOUTON RAFRAÎCHIR EN BAS ==========
        refresh_button = ctk.CTkButton(
            self,
            text="🔄 Rafraîchir les données",
            font=("Arial", 14, "bold"),
            width=200,
            height=45,
            corner_radius=25,
            fg_color="#e67e22",
            hover_color="#d35400",
            text_color="white",
            command=self.manual_refresh
        )
        refresh_button.pack(pady=(10, 15))

        # Label pour la dernière mise à jour
        self.update_label = ctk.CTkLabel(
            self, 
            text="Dernière mise à jour: --",
            font=("Arial", 11),
            text_color="gray"
        )
        self.update_label.pack(pady=(0, 10))

    def create_stat_cards(self, stats):
        """Crée les cartes de statistiques"""
        # Nettoyer les anciennes cartes
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Configuration des cartes
        cards_config = [
            {"title": "🏨 Chambres", "value": stats['total_chambres'], "subtitle": "Total chambres", "color": "#e67e22"},
            {"title": "🟢 Libres", "value": stats['chambres_libres'], "subtitle": "Disponibles", "color": "#2ecc71"},
            {"title": "🔴 Occupées", "value": stats['chambres_occupees'], "subtitle": f"Taux: {stats['taux_occupation']}%", "color": "#e74c3c"},
            {"title": "🧹 Nettoyage", "value": stats['chambres_nettoyage'], "subtitle": "En cours", "color": "#f39c12"},
            {"title": "👥 Clients", "value": stats['total_clients'], "subtitle": "Inscrits", "color": "#e67e22"},
            {"title": "📅 Réservations", "value": f"{stats['reservations_actives']}/{stats['reservations_total']}", "subtitle": "Actives/Total", "color": "#e67e22"},
            {"title": "💰 CA Total", "value": f"{stats['ca_total']:,.0f} €", "subtitle": "Chiffre d'affaires", "color": "#e67e22"},
            {"title": "📆 CA du mois", "value": f"{stats['ca_mois']:,.0f} €", "subtitle": "Ce mois", "color": "#e67e22"},
        ]

        # Création des cartes en grille (2 lignes x 4 colonnes)
        row = 0
        col = 0
        for card in cards_config:
            card_frame = ctk.CTkFrame(
                self.cards_frame,
                corner_radius=15,
                border_width=2,
                border_color=card["color"],
                fg_color="#1a1a2e",
                width=200,
                height=120
            )
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card_frame.grid_propagate(False)

            # Titre
            ctk.CTkLabel(
                card_frame,
                text=card["title"],
                font=("Arial", 14, "bold"),
                text_color=card["color"]
            ).pack(pady=(10, 5))

            # Valeur
            ctk.CTkLabel(
                card_frame,
                text=str(card["value"]),
                font=("Arial", 24, "bold"),
                text_color="white"
            ).pack(pady=(5, 5))

            # Sous-titre
            ctk.CTkLabel(
                card_frame,
                text=card["subtitle"],
                font=("Arial", 11),
                text_color="gray"
            ).pack()

            col += 1
            if col >= 4:
                col = 0
                row += 1

        # Configurer les colonnes pour qu'elles s'étendent uniformément
        for i in range(4):
            self.cards_frame.grid_columnconfigure(i, weight=1)

    def create_stats_section(self, stats):
        """Crée la section des statistiques détaillées"""
        # Nettoyer l'ancien contenu
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Frame gauche - Répartition par type
        left_frame = ctk.CTkFrame(self.stats_frame, corner_radius=15, border_width=1, border_color="#e67e22")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        ctk.CTkLabel(
            left_frame,
            text="📊 Répartition des chambres par type",
            font=("Arial", 16, "bold"),
            text_color="#e67e22"
        ).pack(pady=(15, 10))

        # Récupérer les données via le contrôleur
        occupation_par_type = self.controller.get_occupation_par_type()
        
        if occupation_par_type:
            for ch_type, statuts in occupation_par_type.items():
                type_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
                type_frame.pack(fill="x", padx=20, pady=5)

                ctk.CTkLabel(
                    type_frame,
                    text=f"{ch_type.upper()} :",
                    font=("Arial", 13, "bold"),
                    width=80
                ).pack(side="left")

                total = sum(statuts.values())
                libre = statuts.get('libre', 0)
                occupee = statuts.get('occupee', 0)
                nettoyage = statuts.get('nettoyage', 0)

                ctk.CTkLabel(
                    type_frame,
                    text=f"Libres {libre}  Occupées {occupee}  Nettoyage {nettoyage}  (Total: {total})",
                    font=("Arial", 12)
                ).pack(side="left", padx=(10, 0))
        else:
            ctk.CTkLabel(
                left_frame,
                text="Aucune donnée disponible",
                font=("Arial", 12),
                text_color="gray"
            ).pack(pady=20)

        # Frame droite - Taux d'occupation
        right_frame = ctk.CTkFrame(self.stats_frame, corner_radius=15, border_width=1, border_color="#e67e22")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

        ctk.CTkLabel(
            right_frame,
            text="📈 Taux d'occupation",
            font=("Arial", 16, "bold"),
            text_color="#e67e22"
        ).pack(pady=(15, 10))

        # Barre de progression pour le taux d'occupation
        taux = stats['taux_occupation']
        
        ctk.CTkLabel(
            right_frame,
            text=f"{taux}%",
            font=("Arial", 36, "bold"),
            text_color="#e67e22" if taux < 80 else "#2ecc71" if taux < 95 else "#e74c3c"
        ).pack(pady=(20, 5))

        progress_bar = ctk.CTkProgressBar(
            right_frame,
            width=250,
            height=20,
            corner_radius=10,
            progress_color="#e67e22"
        )
        progress_bar.pack(pady=10)
        progress_bar.set(taux / 100)

        ctk.CTkLabel(
            right_frame,
            text=f"{stats['chambres_occupees']} chambres occupées sur {stats['total_chambres']}",
            font=("Arial", 12),
            text_color="gray"
        ).pack()

        # CA du mois
        ctk.CTkLabel(
            right_frame,
            text="💰 Chiffre d'affaires",
            font=("Arial", 14, "bold"),
            text_color="#27ae60"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            right_frame,
            text=f"{stats['ca_mois']:,.0f} €",
            font=("Arial", 20, "bold"),
            text_color="#27ae60"
        ).pack()

        ctk.CTkLabel(
            right_frame,
            text="Ce mois",
            font=("Arial", 11),
            text_color="gray"
        ).pack()

    def create_tables_section(self):
        """Crée la section des tableaux récents"""
        # Nettoyer l'ancien contenu
        for widget in self.tables_frame.winfo_children():
            widget.destroy()

        # Style pour les Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # Frame gauche - Dernières réservations
        left_frame = ctk.CTkFrame(self.tables_frame, corner_radius=15, border_width=1, border_color="#e67e22")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        ctk.CTkLabel(
            left_frame,
            text="📅 Dernières réservations",
            font=("Arial", 14, "bold"),
            text_color="#e67e22"
        ).pack(pady=(10, 5))

        # Treeview pour les réservations
        columns_res = ("client", "chambre", "arrivee", "depart", "statut")
        tree_res = ttk.Treeview(left_frame, columns=columns_res, show="headings", height=8)
        
        col_configs_res = {
            "client": {"text": "Client", "width": 150},
            "chambre": {"text": "Chambre", "width": 80},
            "arrivee": {"text": "Arrivée", "width": 100},
            "depart": {"text": "Départ", "width": 100},
            "statut": {"text": "Statut", "width": 80}
        }
        
        for col, config in col_configs_res.items():
            tree_res.heading(col, text=config["text"])
            tree_res.column(col, width=config["width"])
        
        # Scrollbar
        scroll_res = ttk.Scrollbar(left_frame, orient="vertical", command=tree_res.yview)
        tree_res.configure(yscrollcommand=scroll_res.set)
        
        tree_res.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scroll_res.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Charger les réservations via le contrôleur
        reservations = self.controller.get_reservations_recentes(8)
        for res in reservations:
            tree_res.insert("", "end", values=(
                res['client_nom'], res['chambre_numero'],
                res['date_arrivee'], res['date_depart'], res['statut']
            ))

        # Frame droite - Dernières factures
        right_frame = ctk.CTkFrame(self.tables_frame, corner_radius=15, border_width=1, border_color="#e67e22")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

        ctk.CTkLabel(
            right_frame,
            text="💰 Dernières factures",
            font=("Arial", 14, "bold"),
            text_color="#e67e22"
        ).pack(pady=(10, 5))

        # Treeview pour les factures
        columns_fact = ("client", "montant", "date", "mode")
        tree_fact = ttk.Treeview(right_frame, columns=columns_fact, show="headings", height=8)
        
        col_configs_fact = {
            "client": {"text": "Client", "width": 150},
            "montant": {"text": "Montant", "width": 100},
            "date": {"text": "Date", "width": 100},
            "mode": {"text": "Mode", "width": 100}
        }
        
        for col, config in col_configs_fact.items():
            tree_fact.heading(col, text=config["text"])
            tree_fact.column(col, width=config["width"])
        
        # Scrollbar
        scroll_fact = ttk.Scrollbar(right_frame, orient="vertical", command=tree_fact.yview)
        tree_fact.configure(yscrollcommand=scroll_fact.set)
        
        tree_fact.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scroll_fact.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Charger les factures via le contrôleur
        factures = self.controller.get_factures_recentes(8)
        for fact in factures:
            tree_fact.insert("", "end", values=(
                fact['client_nom'], f"{fact['montant_total']:.2f} €",
                fact['date_paiement'] or "Non payée", fact['mode_paiement'] or "-"
            ))

    def load_data(self):
        """Charge toutes les données via le contrôleur"""
        # Récupérer toutes les statistiques
        stats = self.controller.get_statuts_cards()
        
        # Mettre à jour l'interface
        self.create_stat_cards(stats)
        self.create_stats_section(stats)
        self.create_tables_section()
        
        # Mettre à jour l'horodatage
        from datetime import datetime
        self.update_label.configure(text=f"Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}")

    def manual_refresh(self):
        """Rafraîchissement manuel (appelé par le bouton)"""
        self.load_data()
        # Animation rapide du bouton pour feedback visuel
        self.update_label.configure(text="🔄 Mise à jour en cours...")
        self.update_idletasks()

    def start_auto_refresh(self):
        """Démarre le rafraîchissement automatique toutes les 30 secondes"""
        self.after(30000, self.refresh_data)
    
    def refresh_data(self):
        """Rafraîchit les données automatiquement"""
        self.load_data()
        self.after(30000, self.refresh_data)