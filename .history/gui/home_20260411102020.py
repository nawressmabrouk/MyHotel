import customtkinter as ctk
from PIL import Image
import os

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, main_app=None):
        super().__init__(parent)
        self.parent = parent
        self.main_app = main_app
        self.cards = []           
        self.cards_enabled = False 
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
            self.configure(fg_color=("#f5f5f5", "#1a1a1a"))

        # === FRAME SCROLLABLE ===
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === CONTENU ===
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)

        # === EN-TÊTE ===
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(30, 20))

        title = ctk.CTkLabel(
            header_frame,
            text="🏨 MyHotel PMS",
            font=("Arial", 44, "bold"),
            text_color=("#1f538d", "#3a7eb6")
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            header_frame,
            text="La solution complète pour la gestion de votre établissement hôtelier",
            font=("Arial", 18),
            text_color=("gray40", "gray70")
        )
        subtitle.pack(pady=(10, 20))

        # === LIGNE DÉCORATIVE ===
        separator = ctk.CTkFrame(content_frame, height=3, fg_color=("#e67e22", "#e67e22"))
        separator.pack(fill="x", padx=200, pady=10)

        # === SECTION DESCRIPTION ===
        desc_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        desc_frame.pack(fill="x", padx=50, pady=30)

        # Paragraphe 1
        desc1 = ctk.CTkLabel(
            desc_frame,
            text="MyHotel est une plateforme moderne et intuitive conçue pour simplifier la gestion quotidienne de votre hôtel. Que vous dirigiez un petit établissement ou un grand complexe hôtelier, notre solution vous offre tous les outils nécessaires pour optimiser vos opérations et offrir une expérience exceptionnelle à vos clients.",
            font=("Arial", 14),
            justify="center",
            wraplength=800
        )
        desc1.pack(pady=10)

        # Paragraphe 2
        desc2 = ctk.CTkLabel(
            desc_frame,
            text="Avec MyHotel, centralisez vos réservations, gérez vos chambres en temps réel, suivez vos clients et automatisez la facturation. Notre interface claire et notre tableau de bord personnalisé vous permettent de prendre des décisions éclairées et d'augmenter votre rentabilité.",
            font=("Arial", 14),
            justify="center",
            wraplength=800
        )
        desc2.pack(pady=10)

        # === SECTION FONCTIONNALITÉS ===
        features_title = ctk.CTkLabel(
            content_frame,
            text=" Ce que vous pouvez faire avec MyHotel ",
            font=("Arial", 22, "bold"),
            text_color=("#e67e22", "#e67e22")
        )
        features_title.pack(pady=(30, 20))

        # === GRILLE DES FONCTIONNALITÉS ===
        features_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        features_container.pack(fill="both", expand=True, padx=40, pady=10)

        features_container.grid_columnconfigure(0, weight=1)
        features_container.grid_columnconfigure(1, weight=1)
        features_container.grid_rowconfigure(0, weight=1)
        features_container.grid_rowconfigure(1, weight=1)

        # Liste des fonctionnalités
        features = [
            {
                "icon": "🛏",
                "title": "Gestion des chambres",
                "desc": "Ajoutez, modifiez ou supprimez des chambres. Suivez leur statut en temps réel (libre, occupée, nettoyage) et définissez les prix par nuit.",
                "color": "#e67e22",
                "tab": "Chambres"
            },
            {
                "icon": "👥",
                "title": "Gestion des clients",
                "desc": "Maintenez un carnet d'adresses complet de vos clients. Recherchez, modifiez ou supprimez des fiches clients facilement.",
                "color": "#e67e22",
                "tab": "Clients"
            },
            {
                "icon": "📅",
                "title": "Gestion des réservations",
                "desc": "Planifiez les séjours de vos clients, vérifiez la disponibilité des chambres et suivez l'état des réservations (active, terminée, annulée).",
                "color": "#e67e22",
                "tab": "Réservations"
            },
            {
                "icon": "💰",
                "title": "Gestion des factures",
                "desc": "Générez automatiquement des factures basées sur la durée du séjour et le prix de la chambre. Exportez vos données en CSV.",
                "color": "#e67e22",
                "tab": "Factures"
            }
        ]

        for i, feature in enumerate(features):
            row, col = divmod(i, 2)
            
            card = ctk.CTkFrame(
                features_container, 
                corner_radius=15, 
                border_width=2,
                border_color=feature["color"],
                fg_color=("white", "#333333"),
                cursor="arrow"
            )
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            self.cards.append(card)

            # Fonction de clic qui vérifie si les cartes sont activées
            def on_card_click(e, t=feature["tab"]):
                if self.cards_enabled:
                    self.go_to_tab(t)

            card.bind("<Button-1>", on_card_click)
            # Animation au survol
            def on_enter(e, c=card, col=feature["color"]):
                c.configure(border_color=col, border_width=3)
            def on_leave(e, c=card, col=feature["color"]):
                c.configure(border_color=col, border_width=2)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            # Icône circulaire
            icon_frame = ctk.CTkFrame(card, width=60, height=60, corner_radius=30, fg_color=feature["color"], bg_color="transparent")
            icon_frame.pack(pady=(20, 10))
            icon_frame.pack_propagate(False)
            
            icon_label = ctk.CTkLabel(icon_frame, text=feature["icon"], font=("Arial", 28), text_color="white")
            icon_label.pack(expand=True)

            # Titre
            title_label = ctk.CTkLabel(card, text=feature["title"], font=("Arial", 18, "bold"), text_color=("#1f538d", "#3a7eb6"))
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

        # === SECTION AVANTAGES ===
        benefits_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        benefits_frame.pack(fill="x", padx=50, pady=40)

        benefits_title = ctk.CTkLabel(
            benefits_frame,
            text="⭐ Pourquoi choisir MyHotel ?",
            font=("Arial", 22, "bold"),
            text_color=("#e67e22", "#e67e22")
        )
        benefits_title.pack(pady=(20, 20))

        # Ligne des avantages
        benefits_container = ctk.CTkFrame(benefits_frame, fg_color="transparent")
        benefits_container.pack(fill="x", pady=10)
        
        benefits_container.grid_columnconfigure(0, weight=1)
        benefits_container.grid_columnconfigure(1, weight=1)
        benefits_container.grid_columnconfigure(2, weight=1)
        benefits_container.grid_columnconfigure(3, weight=1)

        benefits = [
            ("⚡", "Simple et rapide", "Interface intuitive"),
            ("🔒", "Sécurisé", "Données protégées"),
            ("📊", "Statistiques", "Tableau de bord complet"),
            ("💡", "Automatisé", "Calculs automatiques")
        ]

        for i, (icon, title_b, desc_b) in enumerate(benefits):
            col = i
            benefit_card = ctk.CTkFrame(benefits_container, corner_radius=10, fg_color=("white", "#2b2b2b"))
            benefit_card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(benefit_card, text=icon, font=("Arial", 32)).pack(pady=(15, 5))
            ctk.CTkLabel(benefit_card, text=title_b, font=("Arial", 14, "bold")).pack()
            ctk.CTkLabel(benefit_card, text=desc_b, font=("Arial", 11), text_color="gray").pack(pady=(0, 15))

        # === PIED DE PAGE ===
        footer_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=20)

        footer_sep = ctk.CTkFrame(footer_frame, height=1, fg_color="gray60")
        footer_sep.pack(fill="x", padx=200, pady=5)

        footer = ctk.CTkLabel(
            footer_frame,
            text="© 2026 - MyHotel - Solution professionnelle de gestion hôtelière",
            font=("Arial", 11),
            text_color="black"
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
    def set_cards_enabled(self, enabled):
        """Active ou désactive le clic sur les cartes"""
        self.cards_enabled = enabled
        # Changer le curseur et l'apparence des cartes
        for card in self.cards:
            if enabled:
                card.configure(cursor="hand2")
            else:
                card.configure(cursor="arrow")