import customtkinter as ctk

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # En-tête avec une bannière légère
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(30, 10))

        title = ctk.CTkLabel(
            header_frame, 
            text="🏨 Gestion d'Hôtel", 
            font=("Arial", 36, "bold"),
            text_color=("#1f538d", "#3a7eb6")  # couleur dynamique selon thème
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Solution complète pour la gestion de votre établissement",
            font=("Arial", 14),
            text_color="gray"
        )
        subtitle.pack(pady=(5, 20))

        # Ligne décorative
        separator = ctk.CTkFrame(self, height=2, fg_color=("#3a7eb6", "#1f538d"))
        separator.pack(fill="x", padx=100, pady=10)

        # Frame pour les cartes de fonctionnalités
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=40, pady=20)

        # Configuration du grid (2x2)
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)
        cards_container.grid_rowconfigure(0, weight=1)
        cards_container.grid_rowconfigure(1, weight=1)

        # Définition des cartes
        features = [
            ("🛏️ Chambres", "Gérer les chambres :\najout, modification,\nsuppression et suivi\n des statuts"),
            ("👥 Clients", "Carnet d'adresses complet :\najout, recherche,\n modification et\n suppression"),
            ("📅 Réservations", "Planifiez les séjours,\nvérifiez la disponibilité,\ngérez les arrivées/départs"),
            ("💰 Factures", "Générez des factures,\ncalculez automatiquement\nle montant, exportez\n les données")
        ]

        for i, (title_text, desc) in enumerate(features):
            row, col = divmod(i, 2)
            card = ctk.CTkFrame(cards_container, corner_radius=15, border_width=1, border_color="gray60")
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            # Titre de la carte
            card_title = ctk.CTkLabel(card, text=title_text, font=("Arial", 20, "bold"))
            card_title.pack(pady=(20, 10))

            # Séparateur interne
            sep = ctk.CTkFrame(card, height=2, fg_color=("#3a7eb6", "#1f538d"))
            sep.pack(fill="x", padx=20, pady=5)

            # Description
            card_desc = ctk.CTkLabel(card, text=desc, font=("Arial", 12), justify="center")
            card_desc.pack(pady=10, padx=15, fill="both", expand=True)

            # Bouton (simple, sans action spécifique)
            btn = ctk.CTkButton(card, text="Accéder", width=120, command=lambda t=title_text: self.go_to_tab(t))
            btn.pack(pady=(10, 20))

        # Pied de page
        footer = ctk.CTkLabel(self, text="© 2026 - Projet Python - Tous droits réservés", font=("Arial", 10), text_color="gray")
        footer.pack(side="bottom", pady=10)

    def go_to_tab(self, feature_name):
        """Navigation vers l'onglet correspondant (optionnel)"""
        tab_mapping = {
            "🛏️ Chambres": "Chambres",
            "👥 Clients": "Clients",
            "📅 Réservations": "Réservations",
            "💰 Factures": "Factures"
        }
        tab_name = tab_mapping.get(feature_name)
        if tab_name and hasattr(self.parent, "tabview"):
            self.parent.tabview.set(tab_name)