import customtkinter as ctk
from PIL import Image
import os

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, main_app=None):
        super().__init__(parent)
        self.parent = parent
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        # === IMAGE DE FOND (optionnelle) ===
        bg_image_path = os.path.join("assets", "background.jpg")
        if os.path.exists(bg_image_path):
            bg_img = Image.open(bg_image_path)
            bg_photo = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(self.winfo_width(), self.winfo_height()))
            self.bg_label = ctk.CTkLabel(self, image=bg_photo, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            # Mettre à jour la taille de l'image quand la fenêtre est redimensionnée
            self.bind("<Configure>", self.resize_background)
        else:
            # Pas d'image : fond dégradé ou couleur unie
            self.configure(fg_color=("#e0e0e0", "#1a1a1a"))  # gris clair en mode light, sombre en dark

        # === CONTENU PAR-DESSUS LE FOND ===
        # Frame principal semi-transparent pour meilleure lisibilité
        overlay_frame = ctk.CTkFrame(self, fg_color=("white", "#2b2b2b"), corner_radius=20)
        overlay_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        # Titre principal
        title = ctk.CTkLabel(
            overlay_frame,
            text="Gestion d'Hôtel",
            font=("Arial", 36, "bold"),
            text_color=("#1f538d", "#3a7eb6")
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            overlay_frame,
            text="Solution complète pour la gestion de votre établissement",
            font=("Arial", 18),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))

        # Ligne décorative
        separator = ctk.CTkFrame(overlay_frame, height=3, fg_color=("#3a7eb6", "#1f538d"))
        separator.pack(fill="x", padx=100, pady=10)

        # === GRILLE DES FONCTIONNALITÉS (2x2) ===
        cards_container = ctk.CTkFrame(overlay_frame, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=40, pady=30)

        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)
        cards_container.grid_rowconfigure(0, weight=1)
        cards_container.grid_rowconfigure(1, weight=1)

        features = [
            ("🛏️ Chambres", "Gérer les chambres :\najout, modification,\nsuppression et suivi\ndes statuts", "Chambres"),
            ("👥 Clients", "Carnet d'adresses complet :\najout, recherche,\nmodification et\nsuppression", "Clients"),
            ("📅 Réservations", "Planifiez les séjours,\nvérifiez la disponibilité,\ngérez les arrivées\net départs", "Réservations"),
            ("💰 Factures", "Générez des factures,\ncalculez automatiquement\nle montant, exportez\nles données", "Factures")
        ]

        for i, (title_text, desc, tab_name) in enumerate(features):
            row, col = divmod(i, 2)
            card = ctk.CTkFrame(cards_container, corner_radius=15, border_width=1, border_color="gray60")
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            # Titre
            ctk.CTkLabel(card, text=title_text, font=("Arial", 22, "bold")).pack(pady=(20, 5))
            # Séparateur
            ctk.CTkFrame(card, height=2, fg_color=("#3a7eb6", "#1f538d")).pack(fill="x", padx=40, pady=5)
            # Description
            ctk.CTkLabel(card, text=desc, font=("Arial", 13), justify="center").pack(pady=15, padx=15, fill="both", expand=True)
            # Bouton
            btn = ctk.CTkButton(
                card, text="Accéder", width=140, height=35,
                command=lambda t=tab_name: self.go_to_tab(t)
            )
            btn.pack(pady=(5, 20))

        # Pied de page
        footer = ctk.CTkLabel(
            overlay_frame,
            text="© 2026 - Projet Python - Tous droits réservés",
            font=("Arial", 11),
            text_color="gray"
        )
        footer.pack(side="bottom", pady=15)

    def resize_background(self, event):
        """Redimensionne l'image de fond quand la fenêtre change de taille"""
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