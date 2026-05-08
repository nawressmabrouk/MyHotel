import os

import customtkinter as ctk
from PIL import Image


class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, main_app=None):
        super().__init__(parent)
        self.parent = parent
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        # === IMAGE DE FOND ===
        bg_image_path = os.path.join("assets", "background.jpg")
        if os.path.exists(bg_image_path):
            bg_img = Image.open(bg_image_path)
            bg_photo = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(self.winfo_width(), self.winfo_height()))
            self.bg_label = ctk.CTkLabel(self, image=bg_photo, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bind("<Configure>", self.resize_background)
        else:
            self.configure(fg_color=("#e0e0e0", "#1a1a1a"))

        # === OVERLAY PRINCIPAL ===
        overlay_frame = ctk.CTkFrame(
            self, 
            fg_color=("#f5f5f5", "#2b2b2b"),
            corner_radius=25,
            border_width=0
        )
        overlay_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # === EN-TÊTE ===
        header_frame = ctk.CTkFrame(overlay_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(30, 10))

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
            font=("Arial", 14),
            text_color=("gray50", "gray70")
        )
        subtitle.pack(pady=(5, 20))

        separator = ctk.CTkFrame(overlay_frame, height=2, fg_color=("#3a7eb6", "#1f538d"))
        separator.pack(fill="x", padx=200, pady=5)

        # === GRILLE DES CARTES ===
        cards_container = ctk.CTkFrame(overlay_frame, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=50, pady=30)

        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)
        cards_container.grid_rowconfigure(0, weight=1)
        cards_container.grid_rowconfigure(1, weight=1)

        # Configuration des cartes
        features = [
            {
                "title": "🛏 Chambres",
                "desc": "Gérer les chambres :\najout, modification,\nsuppression et suivi\ndes statuts",
                "color": "#e67e22",
                "tab": "Chambres"
            },
            {
                "title": "👥 Clients",
                "desc": "Carnet d'adresses complet :\najout, recherche,\nmodification et\nsuppression",
                "color": "#e67e22",
                "tab": "Clients"
            },
            {
                "title": "📅 Réservations",
                "desc": "Planifiez les séjours,\nvérifiez la disponibilité,\ngérez les arrivées\net départs",
                "color": "#e67e22",
                "tab": "Réservations"
            },
            {
                "title": "💰 Factures",
                "desc": "Générez des factures,\ncalculez automatiquement\nle montant, exportez\nles données",
                "color": "#e67e22",
                "tab": "Factures"
            }
        ]

        for i, feature in enumerate(features):
            row, col = divmod(i, 2)
            
            # Carte cliquable
            card = ctk.CTkFrame(
                cards_container, 
                corner_radius=15, 
                border_width=2,
                border_color=feature["color"],
                fg_color=("white", "#333333"),
                cursor="hand2"  # curseur main
            )
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            
            # Lier le clic sur la carte à la navigation
            def on_card_click(t=feature["tab"]):
                self.go_to_tab(t)
            
            card.bind("<Button-1>", lambda e, t=feature["tab"]: self.go_to_tab(t))
            
            # Animation au survol
            def on_enter(e, c=card, col=feature["color"]):
                c.configure(border_color=col, border_width=3)
            
            def on_leave(e, c=card, col=feature["color"]):
                c.configure(border_color=col, border_width=2)
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            # === CONTENU DE LA CARTE ===
            
            # Icône circulaire
            icon_frame = ctk.CTkFrame(
                card, 
                width=70, 
                height=70,
                corner_radius=35,
                fg_color=feature["color"],
                bg_color="transparent"
            )
            icon_frame.pack(pady=(20, 10))
            icon_frame.pack_propagate(False)
            
            # Empêcher le clic sur l'icône de "remonter" (optionnel)
            icon_frame.bind("<Button-1>", lambda e, t=feature["tab"]: self.go_to_tab(t))
            
            icon_label = ctk.CTkLabel(
                icon_frame, 
                text=feature["title"][0:2],  # 🛏️ ou 👥 etc.
                font=("Arial", 32),
                text_color="white",
                bg_color="transparent"
            )
            icon_label.pack(expand=True)
            icon_label.bind("<Button-1>", lambda e, t=feature["tab"]: self.go_to_tab(t))

            # Titre
            title_label = ctk.CTkLabel(
                card, 
                text=feature["title"], 
                font=("Arial", 22, "bold"),
                text_color=("#1f538d", "#3a7eb6")
            )
            title_label.pack(pady=(10, 5))
            title_label.bind("<Button-1>", lambda e, t=feature["tab"]: self.go_to_tab(t))

            # Séparateur
            sep = ctk.CTkFrame(card, height=2, fg_color=feature["color"])
            sep.pack(fill="x", padx=40, pady=5)
            sep.bind("<Button-1>", lambda e, t=feature["tab"]: self.go_to_tab(t))

            # Description
            desc_label = ctk.CTkLabel(
                card, 
                text=feature["desc"], 
                font=("Arial", 12),
                justify="center",
                text_color=("gray30", "gray70")
            )
            desc_label.pack(pady=15, padx=15, fill="both", expand=True)
            desc_label.bind("<Button-1>", lambda e, t=feature["tab"]: self.go_to_tab(t))

            # Bouton
            btn = ctk.CTkButton(
                card, 
                text="Accéder →", 
                width=140, 
                height=38,
                corner_radius=19,
                fg_color=feature["color"],
                hover_color="#2c3e50",
                font=("Arial", 13, "bold"),
                command=lambda t=feature["tab"]: self.go_to_tab(t)
            )
            btn.pack(pady=(5, 25))

        # === PIED DE PAGE ===
        footer_frame = ctk.CTkFrame(overlay_frame, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", pady=15)

        footer_sep = ctk.CTkFrame(footer_frame, height=1, fg_color="gray60")
        footer_sep.pack(fill="x", padx=200, pady=5)

        footer = ctk.CTkLabel(
            footer_frame,
            text="© 2026 - Projet Python - Tous droits réservés",
            font=("Arial", 11),
            text_color=("gray50", "gray60")
        )
        footer.pack(pady=5)

    def resize_background(self, event):
        if hasattr(self, 'bg_label') and self.bg_label:
            new_size = (event.width, event.height)
            bg_path = os.path.join("assets", "background.jpg")
            if os.path.exists(bg_path):
                img = Image.open(bg_path)
                img = img.resize(new_size, Image.LANCZOS)
                new_photo = ctk.CTkImage(light_image=img, dark_image=img, size=new_size)
                self.bg_label.configure(image=new_photo)
                self.bg_label.image = new_photo

    def go_to_tab(self, tab_name):
        if self.main_app and hasattr(self.main_app, "switch_to_tab"):
            self.main_app.switch_to_tab(tab_name)
            
    def on_enter(e, b=btn):
        if self.current_tab != tab_name:
            b.configure(border_width=2, border_color="#3a7eb6")
    def on_leave(e, b=btn):
        if self.current_tab != tab_name:
           b.configure(border_width=0)
   btn.bind("<Enter>", on_enter)
   btn.bind("<Leave>", on_leave)            