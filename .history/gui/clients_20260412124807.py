import os
import sys
from fileinput import filename

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csv
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk

from controllers.clients_controller import ClientsController


class ClientsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = ClientsController()
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # ========== STYLE AMÉLIORÉ POUR LE TREEVIEW ==========
        style = ttk.Style()
        style.theme_use("clam")
        
        # Style pour l'en-tête
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 12, "bold"),
            background="#e67e22",
            foreground="white",
            padding=8,
            borderwidth=0
        )
        
        # Style pour les lignes
        style.configure(
            "Treeview",
            font=("Segoe UI", 11),
            rowheight=35,
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0,
            highlightthickness=0
        )
        
        # Style pour la sélection
        style.map(
            "Treeview",
            background=[("selected", "#e67e22")],
            foreground=[("selected", "white")]
        )
        
        # Alternance des couleurs des lignes
        style.tag_configure("odd", background="#333333")
        style.tag_configure("even", background="#2b2b2b")

        # ========== CONTENEUR PRINCIPAL ==========
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # ========== TITRE DE LA SECTION ==========
        title_label = ctk.CTkLabel(
            main_container,
            text="👥 Gestion des Clients",
            font=("Segoe UI", 22, "bold"),
            text_color="#e67e22"
        )
        title_label.pack(anchor="w", pady=(0, 15))

        # ========== TABLEAU AVEC BORDURE MODERNE ==========
        table_container = ctk.CTkFrame(
            main_container, 
            corner_radius=20,
            border_width=2,
            border_color="#e67e22",
            fg_color="#1a1a2e"
        )
        table_container.pack(fill="both", expand=True, pady=(0, 15))

        # Configuration des colonnes
        columns = ("id", "nom", "email", "telephone", "adresse")
        self.tree = ttk.Treeview(
            table_container, 
            columns=columns, 
            show="headings", 
            height=18,
            selectmode="browse"
        )
        
        # Configuration des colonnes avec meilleures largeurs
        column_configs = {
            "id": {"text": "ID", "width": 60, "anchor": "center"},
            "nom": {"text": "Nom complet", "width": 200, "anchor": "w"},
            "email": {"text": "Adresse email", "width": 220, "anchor": "w"},
            "telephone": {"text": "Téléphone", "width": 130, "anchor": "center"},
            "adresse": {"text": "Adresse", "width": 250, "anchor": "w"}
        }
        
        for col, config in column_configs.items():
            self.tree.heading(col, text=config["text"])
            self.tree.column(col, width=config["width"], anchor=config["anchor"])

        # Scrollbars stylisées
        v_scroll = ttk.Scrollbar(
            table_container, 
            orient="vertical", 
            command=self.tree.yview,
            style="Vertical.TScrollbar"
        )
        h_scroll = ttk.Scrollbar(
            table_container, 
            orient="horizontal", 
            command=self.tree.xview,
            style="Horizontal.TScrollbar"
        )
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Placement
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        v_scroll.grid(row=0, column=1, sticky="ns", pady=10)
        h_scroll.grid(row=1, column=0, sticky="ew", padx=10)
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # ========== BARRE D'OUTILS (BOUTONS) ==========
        toolbar = ctk.CTkFrame(main_container, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 15))

        # Frame pour les boutons d'action
        actions_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        actions_frame.pack(side="left", fill="x", expand=True)

        buttons = [
            ("➕ Ajouter", "#27ae60", self.add),
            ("✏️ Modifier", "#e67e22", self.edit),
            ("🗑️ Supprimer", "#e74c3c", self.delete),
            ("🔄 Rafraîchir", "#3498db", self.load_data),
            ("📎 Exporter CSV", "#9b59b6", self.export_csv)
        ]
        
        for text, color, command in buttons:
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                font=("Segoe UI", 13, "bold"),
                width=130,
                height=40,
                corner_radius=12,
                fg_color=color,
                hover_color="#2c3e50",
                command=command
            )
            btn.pack(side="left", padx=5)

        # ========== BARRE DE RECHERCHE ==========
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.pack(side="right")

        ctk.CTkLabel(
            search_frame, 
            text="🔍", 
            font=("Segoe UI", 16),
            text_color="#e67e22"
        ).pack(side="left", padx=(0, 8))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            textvariable=self.search_var, 
            width=220,
            height=40,
            corner_radius=12,
            placeholder_text="Rechercher un client...",
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            search_frame, 
            text="Rechercher", 
            width=100,
            height=40,
            corner_radius=12,
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.search,
            font=("Segoe UI", 12, "bold")
        )
        search_btn.pack(side="left", padx=5)

        reset_btn = ctk.CTkButton(
            search_frame, 
            text="Réinitialiser", 
            width=100,
            height=40,
            corner_radius=12,
            fg_color="#7f8c8d",
            hover_color="#6c7a7a",
            command=self.load_data,
            font=("Segoe UI", 12, "bold")
        )
        reset_btn.pack(side="left", padx=5)

        # ========== BARRE D'INFORMATION ==========
        info_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=30)
        info_frame.pack(fill="x", pady=(0, 0))

        self.info_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=("Segoe UI", 12),
            text_color="#95a5a6"
        )
        self.info_label.pack(side="left")

    def load_data(self):
        """Charge tous les clients via le contrôleur"""
        # Supprimer les anciennes données
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        rows = self.controller.get_all_clients()
        
        if rows:
            for i, r in enumerate(rows):
                # Alternance des couleurs des lignes
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=(
                    r['id'], 
                    r['nom'], 
                    r['email'], 
                    r['telephone'] or "—", 
                    r['adresse'] or "—"
                ), tags=(tag,))
            self.info_label.configure(
                text=f"📊 {len(rows)} client(s) trouvé(s) | Dernière mise à jour: {self.get_current_time()}",
                text_color="#2ecc71"
            )
        else:
            self.info_label.configure(
                text="📊 Aucun client trouvé",
                text_color="#e74c3c"
            )
        
        # Appliquer les tags pour l'alternance des couleurs
        self.tree.tag_configure("odd", background="#2d2d2d")
        self.tree.tag_configure("even", background="#252525")

    def get_current_time(self):
        """Retourne l'heure actuelle formatée"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    def search(self):
        """Recherche des clients via le contrôleur"""
        term = self.search_var.get().strip()
        
        # Supprimer les anciennes données
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if term:
            rows = self.controller.search_clients_by_nom(term)
        else:
            rows = self.controller.get_all_clients()
        
        if rows:
            for i, r in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", "end", values=(
                    r['id'], 
                    r['nom'], 
                    r['email'], 
                    r['telephone'] or "—", 
                    r['adresse'] or "—"
                ), tags=(tag,))
            self.info_label.configure(
                text=f"📊 {len(rows)} résultat(s) trouvé(s) pour '{term}'",
                text_color="#2ecc71"
            )
        else:
            self.info_label.configure(
                text=f"📊 Aucun résultat trouvé pour '{term}'",
                text_color="#e74c3c"
            )

    def add(self):
        self.open_form()

    def edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un client.")
            return
        item = self.tree.item(selected[0])
        client_id = item['values'][0]
        self.open_form(client_id)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un client.")
            return
        
        if messagebox.askyesno("Confirmation", "Supprimer ce client ? Ses réservations seront aussi supprimées."):
            item = self.tree.item(selected[0])
            client_id = item['values'][0]
            self.controller.delete_client(client_id)
            self.load_data()
            messagebox.showinfo("Succès", "Client supprimé avec succès !")

    def open_form(self, client_id=None):
        """Ouvre le formulaire d'ajout/modification"""
        win = ctk.CTkToplevel(self)
        win.title("Ajouter / Modifier un client")
        win.geometry("500x550")
        win.resizable(False, False)
        win.grab_set()
        
        # Centrer la fenêtre
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (500 // 2)
        y = (win.winfo_screenheight() // 2) - (550 // 2)
        win.geometry(f"500x550+{x}+{y}")

        # Variables
        nom_var = ctk.StringVar()
        email_var = ctk.StringVar()
        telephone_var = ctk.StringVar()
        adresse_var = ctk.StringVar()

        # Si modification, charger les données via le contrôleur
        if client_id:
            row = self.controller.get_client_for_form(client_id)
            if row:
                nom_var.set(row['nom'])
                email_var.set(row['email'])
                telephone_var.set(row['telephone'] or '')
                adresse_var.set(row['adresse'] or '')

        # Titre avec icône
        title_text = "✏️ Modifier un client" if client_id else "➕ Ajouter un client"
        ctk.CTkLabel(
            win, 
            text=title_text, 
            font=("Segoe UI", 22, "bold"),
            text_color="#e67e22"
        ).pack(pady=(25, 20))

        # Frame pour le formulaire
        form_frame = ctk.CTkFrame(win, fg_color="transparent")
        form_frame.pack(padx=35, fill="x")

        # Champ Nom
        ctk.CTkLabel(form_frame, text="Nom complet", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, padx=5, pady=10, sticky="w")
        entry_nom = ctk.CTkEntry(form_frame, textvariable=nom_var, width=380, height=40, corner_radius=10, placeholder_text="Ex: Jean Dupont")
        entry_nom.grid(row=1, column=0, padx=5, pady=(0, 15))

        # Champ Email
        ctk.CTkLabel(form_frame, text="Adresse email", font=("Segoe UI", 13, "bold")).grid(row=2, column=0, padx=5, pady=10, sticky="w")
        entry_email = ctk.CTkEntry(form_frame, textvariable=email_var, width=380, height=40, corner_radius=10, placeholder_text="Ex: jean@example.com")
        entry_email.grid(row=3, column=0, padx=5, pady=(0, 15))

        # Champ Téléphone
        ctk.CTkLabel(form_frame, text="Téléphone", font=("Segoe UI", 13, "bold")).grid(row=4, column=0, padx=5, pady=10, sticky="w")
        entry_telephone = ctk.CTkEntry(form_frame, textvariable=telephone_var, width=380, height=40, corner_radius=10, placeholder_text="Ex: 06 12 34 56 78")
        entry_telephone.grid(row=5, column=0, padx=5, pady=(0, 15))

        # Champ Adresse
        ctk.CTkLabel(form_frame, text="Adresse", font=("Segoe UI", 13, "bold")).grid(row=6, column=0, padx=5, pady=10, sticky="w")
        entry_adresse = ctk.CTkEntry(form_frame, textvariable=adresse_var, width=380, height=40, corner_radius=10, placeholder_text="Ex: 10 rue de Paris, 75001 Paris")
        entry_adresse.grid(row=7, column=0, padx=5, pady=(0, 15))

        def save():
            nom = entry_nom.get().strip()
            email = entry_email.get().strip()
            telephone = entry_telephone.get().strip()
            adresse = entry_adresse.get().strip()

            is_valid, error_msg = self.controller.validate_nom(nom)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_nom.focus()
                return

            is_valid, error_msg = self.controller.validate_email(email)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_email.focus()
                return

            if self.controller.check_email_exists(email, client_id):
                messagebox.showerror("Erreur", "Cet email est déjà utilisé par un autre client.")
                entry_email.focus()
                return

            telephone = self.controller.format_telephone(telephone)
            adresse = adresse if adresse else None

            if client_id:
                result = self.controller.update_client(client_id, nom, email, telephone, adresse)
            else:
                result = self.controller.add_client(nom, email, telephone, adresse)

            if result is not None:
                win.destroy()
                self.load_data()
                messagebox.showinfo("Succès", "Client enregistré avec succès !")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'enregistrement.")

        # Bouton Enregistrer
        ctk.CTkButton(
            win, 
            text="💾 Enregistrer", 
            command=save, 
            fg_color="#27ae60", 
            hover_color="#219a52", 
            corner_radius=12,
            width=220,
            height=45,
            font=("Segoe UI", 14, "bold")
        ).pack(pady=30)

        entry_nom.focus()

    def export_csv(self):
        data = []
        for child in self.tree.get_children():
            values = self.tree.item(child)['values']
            data.append(values)
    
        if not data:
            messagebox.showwarning("Export", "Aucune donnée à exporter.")
            return
    
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="clients.csv",
            title="Enregistrer le fichier CSV"
        )
    
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nom", "Email", "Téléphone", "Adresse"])
                writer.writerows(data)
            messagebox.showinfo("Export", f"Exporté vers : {os.path.basename(filename)}")