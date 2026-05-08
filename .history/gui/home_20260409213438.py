import customtkinter as ctk

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, main_app=None):
        super().__init__(parent)
        self.parent = parent
        self.main_app = main_app
        self.create_widgets()

    def create_widgets(self):
        # ========== EN-TÊTE HERO ==========
        hero_frame = ctk.CTkFrame(self, fg_color="transparent")
        hero_frame.pack(fill="x", padx=40, pady=(50, 30))

        # Titre principal
        title = ctk.CTkLabel(
            hero_frame,
            text="🏨 MyHotel PMS",
            font=("Arial", 48, "bold"),
            text_color=("#1f538d", "#3a7eb6")
        )
        title.pack()

        # Slogan
        slogan = ctk.CTkLabel(
            hero_frame,
            text="Créons ensemble votre écosystème hôtelier\nsur une plateforme ouverte et automatisable",
            font=("Arial", 20),
            justify="center"
        )
        slogan.pack(pady=(10, 20))

        # Bouton principal (appel à l'action)
        demo_btn = ctk.CTkButton(
            hero_frame,
            text="📞 RÉSERVER UNE DÉMO",
            font=("Arial", 16, "bold"),
            width=250,
            height=50,
            corner_radius=25,
            fg_color="#2c7da0",
            hover_color="#1f5e7a"
        )
        demo_btn.pack(pady=10)

        # ========== GRILLE DES FONCTIONNALITÉS ==========
        features_container = ctk.CTkFrame(self, fg_color="transparent")
        features_container.pack(fill="x", padx=40, pady=40)

        # Configuration en 2 colonnes
        features_container.grid_columnconfigure(0, weight=1)
        features_container.grid_columnconfigure(1, weight=1)

        features = [
            ("🔌 Intégrations", "Intégrez en un clic vos applications préférées"),
            ("⚙️ Automatisations", "Facilitez le travail des équipes avec des scénarios d'automatisation"),
            ("💳 Paiements sécurisés", "Sécurisez vos revenus avec le paiement intégré"),
            ("📊 Tableau de bord", "Suivez en temps réel les indicateurs de votre hôtel")
        ]

        for i, (title_text, desc) in enumerate(features):
            row, col = divmod(i, 2)
            card = ctk.CTkFrame(features_container, corner_radius=10, border_width=1, border_color="gray60")
            card.grid(row=row, column=col, padx=15, pady=15, sticky="ew")

            label_title = ctk.CTkLabel(card, text=title_text, font=("Arial", 18, "bold"))
            label_title.pack(pady=(15, 5))

            label_desc = ctk.CTkLabel(card, text=desc, font=("Arial", 12), wraplength=350, justify="center")
            label_desc.pack(pady=(0, 15))

        # ========== SECTION DES LIENS / FOOTER ==========
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", side="bottom", pady=20)

        # Ligne de séparation
        sep = ctk.CTkFrame(footer_frame, height=2, fg_color="gray40")
        sep.pack(fill="x", padx=200, pady=10)

        # Liens (simulés avec des labels cliquables – optionnel)
        links_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        links_frame.pack()

        links = ["Topsys", "Apaleo Store", "Services", "Ressources", "CONTACT & DÉMO"]
        for link in links:
            lbl = ctk.CTkLabel(links_frame, text=link, font=("Arial", 12), cursor="hand2")
            lbl.pack(side="left", padx=15)
            # On peut ajouter un bind pour ouvrir des URLs plus tard

        # Copyright
        copyright_lbl = ctk.CTkLabel(
            footer_frame,
            text="© 2025 MyHotel PMS - Projet Python",
            font=("Arial", 10),
            text_color="gray"
        )
        copyright_lbl.pack(pady=10)

    def go_to_tab(self, tab_name):
        if self.main_app and hasattr(self.main_app, "switch_to_tab"):
            self.main_app.switch_to_tab(tab_name)