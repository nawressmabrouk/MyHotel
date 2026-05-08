from tkinter import messagebox

import customtkinter as ctk

from controllers.admin_controller import login_admin


class LoginView(ctk.CTkToplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        
        self.parent = parent
        self.on_success = on_success
        
        self.title("Connexion - MyHotel")
        self.geometry("420x500")
        self.resizable(False, False)
        
        # Centre la fenêtre par rapport à l'écran
        self.after(10, self._center)
        
        # Empêche la fermeture sans login
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        
        self.create_widgets()
        
        # Rendre la fenêtre modale
        self.grab_set()
        self.focus()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo / Icône
        icon_label = ctk.CTkLabel(
            main_frame, 
            text="🏨", 
            font=("Arial", 60),
            text_color="#e67e22"
        )
        icon_label.pack(pady=(30, 10))
        
        # Titre
        title = ctk.CTkLabel(
            main_frame,
            text="MyHotel",
            font=("Arial", 28, "bold"),
            text_color="#e67e22"
        )
        title.pack(pady=(0, 5))
        
        # Sous-titre
        subtitle = ctk.CTkLabel(
            main_frame,
            text="Gestion hôtelière professionnelle",
            font=("Arial", 12),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))
        
        # Ligne décorative
        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#e67e22")
        separator.pack(fill="x", padx=50, pady=(0, 30))
        
        # Frame formulaire
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")
        
        # Champ utilisateur
        ctk.CTkLabel(
            form_frame, 
            text="Nom d'utilisateur", 
            font=("Arial", 13, "bold"),
            text_color="#1a1a2e"
        ).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Entrez votre nom d'utilisateur",
            height=42,
            font=("Arial", 13)
        )
        self.username_entry.pack(fill="x", pady=(0, 20))
        
        # Champ mot de passe
        ctk.CTkLabel(
            form_frame, 
            text="Mot de passe", 
            font=("Arial", 13, "bold"),
            text_color="#1a1a2e"
        ).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Entrez votre mot de passe",
            show="*",
            height=42,
            font=("Arial", 13)
        )
        self.password_entry.pack(fill="x", pady=(0, 25))
        
        # Bouton de connexion
        self.login_btn = ctk.CTkButton(
            main_frame,
            text="Se connecter",
            font=("Arial", 14, "bold"),
            height=45,
            corner_radius=10,
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.login
        )
        self.login_btn.pack(padx=50, pady=(10, 15), fill="x")
        
        # Message d'erreur
        self.error_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.error_label.pack()
        
        # Info test
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(pady=(20, 10))
        
        ctk.CTkLabel(
            info_frame,
            text="🔑 Identifiants de test",
            font=("Arial", 11),
            text_color="gray"
        ).pack()
        
        ctk.CTkLabel(
            info_frame,
            text="Utilisateur : admin  |  Mot de passe : admin123",
            font=("Arial", 11),
            text_color="#e67e22"
        ).pack()
        
        # Lier la touche Entrée
        self.bind("<Return>", lambda e: self.login())
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Désactiver le bouton
        self.login_btn.configure(state="disabled", text="Connexion en cours...")
        self.error_label.configure(text="")
        self.update_idletasks()
        
        if not username or not password:
            self.error_label.configure(text="❌ Veuillez remplir tous les champs")
            self.login_btn.configure(state="normal", text="Se connecter")
            return
        
        admin = login_admin(username, password)
        
        if admin:
            # Connexion réussie
            self.destroy()
            self.on_success(admin)
        else:
            self.error_label.configure(text="❌ Identifiants incorrects")
            self.password_entry.delete(0, "end")
            self.password_entry.focus()
            self.login_btn.configure(state="normal", text="Se connecter")
    
    def quit_app(self):
        """Quitte complètement l'application"""
        import sys
        sys.exit(0)
    
    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")