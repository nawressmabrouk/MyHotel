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

        # === OVERLAY (fond semi-transparent simulé avec une couleur unie) ===
        # CustomTkinter ne gère pas la transparence, on utilise une couleur unie
        overlay_frame = ctk.CTkFrame(
            self, 
            fg_color=("#f0f0f0", "#2b2b2b"),  # gris clair en mode light, sombre en dark
            corner_radius=20,
            border_width=2,
            border_color=("#3a7eb6", "#1f538d")
        )
        overlay_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        # Titre
        title = ctk.CTkLabel(
            overlay_frame,
            text="🏨 Gestion d'Hôtel",
            font=("Arial", 38, "bold"),
            text_color=("#1f538d", "#3a7eb6")
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            overlay_frame,
            text="Solution complète pour la gestion de votre établissement",
            font=("Arial", 16),
            text_color=("gray20", "gray80")
        )
        subtitle.pack(pady=(0, 30))

        separator = ctk.CTkFrame(overlay_frame, height=3, fg_color=("#3a7eb6", "#1f538d"))
        separator.pack(fill="x", padx=100, pady=10)

        # === GRILLE DES CARTES ===
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
            card = ctk.CTkFrame(
                cards_container, 
                corner_radius=12, 
                border_width=1, 
                border_color=("#3a7eb6", "#555555"),
                fg_color=("white", "#3a3a3a")
            )
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            ctk.CTkLabel(card, text=title_text, font=("Arial", 20, "bold")).pack(pady=(20, 5))
            ctk.CTkFrame(card, height=2, fg_color=("#3a7eb6", "#1f538d")).pack(fill="x", padx=40, pady=5)
            ctk.CTkLabel(card, text=desc, font=("Arial", 12), justify="center").pack(pady=15, padx=15, fill="both", expand=True)
            
            btn = ctk.CTkButton(
                card, text="Accéder", width=140, height=35,
                command=lambda t=tab_name: self.go_to_tab(t)
            )
            btn.pack(pady=(5, 20))

        # Pied de page
        footer = ctk.CTkLabel(
            overlay_frame,
            text="© 2025 - Projet Python - Tous droits réservés",
            font=("Arial", 11),
            text_color=("gray40", "gray60")
        )
        footer.pack(side="bottom", pady=15)

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