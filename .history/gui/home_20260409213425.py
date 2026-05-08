import customtkinter as ctk

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, main_app=None):
        super().__init__(parent)
        self.parent = parent
        self.main_app = main_app  # référence à la fenêtre principale
        self.create_widgets()

    def create_widgets(self):
        # En-tête
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(40, 10))

        title = ctk.CTkLabel(
            header_frame,
            text="🏨 Gestion d'Hôtel",
            font=("Arial", 40, "bold"),
            text_color=("#1f538d", "#3a7eb6")
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Solution complète pour la gestion de votre établissement",
            font=("Arial", 16),
            text_color="gray"
        )
        subtitle.pack(pady=(5, 30))

        # Ligne décorative
        separator = ctk.CTkFrame(self, height=3, fg_color=("#3a7eb6", "#1f538d"))
        separator.pack(fill="x", padx=150, pady=10)

        # Frame pour les cartes
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=50, pady=20)

        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)
        cards_container.grid_rowconfigure(0, weight=1)
        cards_container.grid_rowconfigure(1, weight=1)

        # Définition des cartes avec les boutons qui fonctionnent
        features = [
            ("🛏️ Chambres", "Gérer les chambres :\najout, modification,\nsuppression et suivi\ndes statuts", "Chambres"),
            ("👥 Clients", "Carnet d'adresses complet :\najout, recherche,\nmodification et\nsuppression", "Clients"),
            ("📅 Réservations", "Planifiez les séjours,\nvérifiez la disponibilité,\ngérez les arrivées\net départs", "Réservations"),
            ("💰 Factures", "Générez des factures,\ncalculez automatiquement\nle montant, exportez\nles données", "Factures")
        ]

        for i, (title_text, desc, tab_name) in enumerate(features):
            row, col = divmod(i, 2)
            card = ctk.CTkFrame(cards_container, corner_radius=15, border_width=2, border_color="gray60")
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            # Titre
            card_title = ctk.CTkLabel(card, text=title_text, font=("Arial", 22, "bold"))
            card_title.pack(pady=(20, 10))

            # Séparateur
            sep = ctk.CTkFrame(card, height=2, fg_color=("#3a7eb6", "#1f538d"))
            sep.pack(fill="x", padx=30, pady=5)

            # Description
            card_desc = ctk.CTkLabel(card, text=desc, font=("Arial", 13), justify="center")
            card_desc.pack(pady=15, padx=15, fill="both", expand=True)

            # Bouton avec commande pour changer d'onglet
            btn = ctk.CTkButton(
                card,
                text="Accéder",
                width=140,
                height=40,
                font=("Arial", 14),
                command=lambda t=tab_name: self.go_to_tab(t)
            )
            btn.pack(pady=(10, 25))

        # Pied de page
        footer = ctk.CTkLabel(
            self,
            text="© 2025 - Projet Python - Tous droits réservés",
            font=("Arial", 11),
            text_color="gray"
        )
        footer.pack(side="bottom", pady=15)

    def go_to_tab(self, tab_name):
        """Change d'onglet via la méthode de la fenêtre principale"""
        if self.main_app and hasattr(self.main_app, "switch_to_tab"):
            self.main_app.switch_to_tab(tab_name)
        else:
            # Fallback : tentative directe
            try:
                self.master.tabview.set(tab_name)
            except:
                pass