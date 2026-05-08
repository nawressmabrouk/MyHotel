import os
import customtkinter as ctk


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, main_app=None):
        super().__init__(parent)
        self.parent = parent
        self.main_app = main_app
        self.cards = []           # Liste des cartes
        self.cards_enabled = False # État des cartes
        self.create_widgets()

    def set_cards_enabled(self, enabled):
        """Active ou désactive le clic sur les cartes"""
        self.cards_enabled = enabled
        for card in self.cards:
            if enabled:
                card.configure(cursor="hand2")
            else:
                card.configure(cursor="arrow")

    def create_widgets(self):
        # Fond simple
        self.configure(fg_color=("#f5f5f5", "#1a1a1a"))

        # Frame scrollable
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Contenu
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # En-tête
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(30, 20))

        # Titre fonctionnalités
        features_title = ctk.CTkLabel(
            content_frame,
            text="Ce que vous pouvez faire avec MyHotel",
            font=("Arial", 22, "bold"),
            text_color="#e67e22"
        )
        features_title.pack(pady=(30, 20))

        # Grille des cartes
        features_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        features_container.pack(fill="both", expand=True, padx=40, pady=10)

        features_container.grid_columnconfigure(0, weight=1)
        features_container.grid_columnconfigure(1, weight=1)
        features_container.grid_rowconfigure(0, weight=1)
        features_container.grid_rowconfigure(1, weight=1)

        features = [
            {"icon": "🛏️", "title": "Gestion des chambres", "desc": "Ajoutez, modifiez ou supprimez des chambres. Suivez leur statut en temps réel.", "color": "#e67e22", "tab": "Chambres"},
            {"icon": "👥", "title": "Gestion des clients", "desc": "Maintenez un carnet d'adresses complet de vos clients. Recherchez, modifiez ou supprimez des fiches clients.", "color": "#e67e22", "tab": "Clients"},
            {"icon": "📅", "title": "Gestion des réservations", "desc": "Planifiez les séjours de vos clients, vérifiez la disponibilité des chambres.", "color": "#e67e22", "tab": "Réservations"},
            {"icon": "💰", "title": "Gestion des factures", "desc": "Générez automatiquement des factures basées sur la durée du séjour.", "color": "#e67e22", "tab": "Factures"}
        ]

        for i, feature in enumerate(features):
            row, col = divmod(i, 2)
            
            card = ctk.CTkFrame(
                features_container, 
                corner_radius=15, 
                border_width=2,
                border_color=feature["color"],
                fg_color=("white", "#2b2b2b"),
                cursor="arrow"
            )
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            
            self.cards.append(card)
            
            def on_card_click(e, t=feature["tab"]):
                if self.cards_enabled:
                    self.go_to_tab(t)
            
            card.bind("<Button-1>", on_card_click)

            def on_enter(e, c=card, col=feature["color"]):
                c.configure(border_color=col, border_width=3)
            def on_leave(e, c=card, col=feature["color"]):
                c.configure(border_color=col, border_width=2)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            # Icône
            icon_frame = ctk.CTkFrame(card, width=60, height=60, corner_radius=30, fg_color=feature["color"], bg_color="transparent")
            icon_frame.pack(pady=(20, 10))
            icon_frame.pack_propagate(False)
            icon_label = ctk.CTkLabel(icon_frame, text=feature["icon"], font=("Arial", 28), text_color="white")
            icon_label.pack(expand=True)

            # Titre
            title_label = ctk.CTkLabel(card, text=feature["title"], font=("Arial", 18, "bold"), text_color=("#1a1a2e", "#1a1a2e"))
            title_label.pack(pady=(5, 5))

            # Séparateur
            sep = ctk.CTkFrame(card, height=2, fg_color=feature["color"])
            sep.pack(fill="x", padx=30, pady=5)

            # Description
            desc_label = ctk.CTkLabel(card, text=feature["desc"], font=("Arial", 12), justify="center", wraplength=280, text_color=("gray30", "gray80"))
            desc_label.pack(pady=15, padx=15, fill="both", expand=True)

            # Bouton
            btn = ctk.CTkButton(card, text="Accéder →", width=130, height=35, corner_radius=17,
                                fg_color=feature["color"], hover_color="#2c3e50",
                                font=("Arial", 12, "bold"), command=lambda t=feature["tab"]: self.go_to_tab(t))
            btn.pack(pady=(5, 20))

        # Pied de page
        footer_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=20)

        footer_sep = ctk.CTkFrame(footer_frame, height=1, fg_color="gray60")
        footer_sep.pack(fill="x", padx=200, pady=5)

        footer = ctk.CTkLabel(
            footer_frame,
            text="© 2026 - MyHotel - Solution professionnelle de gestion hôtelière",
            font=("Arial", 11),
            text_color="gray"
        )
        footer.pack(pady=5)

    def go_to_tab(self, tab_name):
        if self.main_app and hasattr(self.main_app, "switch_to_tab"):
            self.main_app.switch_to_tab(tab_name)