import customtkinter as ctk

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Titre principal
        title = ctk.CTkLabel(self, text="Bienvenue dans l'application", font=("Arial", 32, "bold"))
        title.pack(pady=(50, 20))

        subtitle = ctk.CTkLabel(self, text="Gestion d'Hôtel", font=("Arial", 24))
        subtitle.pack(pady=10)

        description = """Cette application vous permet de gérer facilement :
- Les chambres (ajout, modification, suppression)
- Les clients (carnet d'adresses)
- Les réservations (planification, disponibilités)
- Les factures (génération et suivi)

Utilisez les onglets ci-dessus pour naviguer."""
        
        desc_label = ctk.CTkLabel(self, text=description, font=("Arial", 14), justify="left")
        desc_label.pack(pady=30, padx=50)

        # Optionnel : une image ou un logo
        # logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(150, 150))
        # logo_label = ctk.CTkLabel(self, image=logo, text="")
        # logo_label.pack(pady=20)

        footer = ctk.CTkLabel(self, text="© 2025 - Projet Python", font=("Arial", 10))
        footer.pack(side="bottom", pady=10)