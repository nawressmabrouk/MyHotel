'''import customtkinter as ctk
from tkinter import messagebox
from controllers.admin_controller import login_admin

class LoginView(ctk.CTkToplevel):
    def __init__(self, on_success):
        super().__init__()

        self.on_success = on_success
        self.title("Connexion - Gestion Hôtel")
        self.geometry("450x400")
        self.resizable(False, False)

        # Centre la fenêtre
        self.after(10, self._center)

        # Empêche la fermeture sans login
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        # ===== CONTENEUR PRINCIPAL =====
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== TITRE =====
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="🏨 Gestion d'Hôtel", 
            font=("Arial", 28, "bold"),
            text_color=("#1f538d", "#3a7eb6")
        )
        title_label.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Veuillez vous connecter",
            font=("Arial", 14),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))

        # ===== FORMULAIRE =====
        form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")

        # Champ utilisateur
        self.username = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Nom d'utilisateur", 
            width=300,
            height=40,
            font=("Arial", 13)
        )
        self.username.pack(pady=(0, 15))

        # Champ mot de passe
        self.password = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Mot de passe", 
            show="*", 
            width=300,
            height=40,
            font=("Arial", 13)
        )
        self.password.pack(pady=(0, 20))

        # ===== BOUTON DE CONNEXION =====
        self.login_btn = ctk.CTkButton(
            self.main_frame,
            text="Se connecter",
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=250,
            height=45,
            font=("Arial", 14, "bold"),
            corner_radius=10,
            command=self.login
        )
        self.login_btn.pack(pady=10)

        # ===== MESSAGE D'ERREUR =====
        self.error_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.error_label.pack()

        # ===== INFO TEST =====
        info_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        info_frame.pack(pady=(25, 10))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="🔐 Identifiants de test : admin / admin123",
            font=("Arial", 11),
            text_color="gray"
        )
        info_label.pack()

        # Permet la touche Entrée pour se connecter
        self.bind("<Return>", lambda e: self.login())
        self.username.focus()

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        self.login_btn.configure(state="disabled", text="Connexion en cours...")
        self.error_label.configure(text="")
        self.update_idletasks()

        if not username or not password:
            self.error_label.configure(text="Veuillez remplir tous les champs")
            self.login_btn.configure(state="normal", text="Se connecter")
            return

        admin = login_admin(username, password)

        if admin:
            self.destroy()
            self.on_success()
        else:
            self.error_label.configure(text="Identifiants incorrects")
            self.password.delete(0, "end")
            self.password.focus()
            self.login_btn.configure(state="normal", text="Se connecter")

    def quit_app(self):
        import sys
        sys.exit(0)

    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")