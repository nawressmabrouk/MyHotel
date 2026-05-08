import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import customtkinter as ctk
from tkinter import filedialog, ttk, messagebox
import csv
from controllers.clients_controller import ClientsController

class ClientsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = ClientsController()  # Instance du contrôleur
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        table_container = ctk.CTkFrame(
            self, 
            corner_radius=15,
            border_width=2,
            border_color="#e67e22",
            fg_color="transparent"
        )
        table_container.pack(fill="both", expand=True, padx=15, pady=15)

        columns = ("id", "nom", "email", "telephone", "adresse")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=18)
        
        column_configs = {
            "id": {"text": "ID", "width": 50, "anchor": "center"},
            "nom": {"text": "Nom", "width": 180, "anchor": "w"},
            "email": {"text": "Email", "width": 200, "anchor": "w"},
            "telephone": {"text": "Téléphone", "width": 120, "anchor": "center"},
            "adresse": {"text": "Adresse", "width": 200, "anchor": "w"}
        }
        
        for col, config in column_configs.items():
            self.tree.heading(col, text=config["text"])
            self.tree.column(col, width=config["width"], anchor=config["anchor"])

        v_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        btn_container = ctk.CTkFrame(self, fg_color="transparent")
        btn_container.pack(fill="x", padx=15, pady=(0, 10))

        btn_frame1 = ctk.CTkFrame(btn_container, fg_color="transparent")
        btn_frame1.pack(pady=5)
        
        buttons = [
            ("➕ Ajouter", "#e67e22", self.add),
            ("✏️ Modifier", "#e67e22", self.edit),
            ("🗑️ Supprimer", "#cd0d03", self.delete),
            ("🔄 Rafraîchir", "#e67e22", self.load_data),
            ("📎 Exporter CSV", "#e67e22", self.export_csv)
        ]
        
        for text, color, command in buttons:
            btn = ctk.CTkButton(
                btn_frame1,
                text=text,
                font=("Arial", 13, "bold"),
                width=140,
                height=40,
                corner_radius=20,
                fg_color=color,
                hover_color="#2c3e50",
                command=command
            )
            btn.pack(side="left", padx=8)

        search_frame = ctk.CTkFrame(btn_container, fg_color="transparent")
        search_frame.pack(pady=10)

        ctk.CTkLabel(
            search_frame, 
            text="🔍 Rechercher par nom :", 
            font=("Arial", 13, "bold"),
            text_color="#e67e22"
        ).pack(side="left", padx=5)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            textvariable=self.search_var, 
            width=250,
            height=38,
            corner_radius=15,
            placeholder_text="Nom du client..."
        )
        self.search_entry.pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame, 
            text="Rechercher", 
            width=120,
            height=38,
            corner_radius=15,
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.search
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame, 
            text="Tout afficher", 
            width=120,
            height=38,
            corner_radius=15,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            command=self.load_data
        ).pack(side="left", padx=5)

        self.info_label = ctk.CTkLabel(
            btn_container,
            text="",
            font=("Arial", 11),
            text_color="gray"
        )
        self.info_label.pack(pady=5)

    def load_data(self):
        """Charge tous les clients via le contrôleur"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        rows = self.controller.get_all_clients()
        
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(
                    r['id'], 
                    r['nom'], 
                    r['email'], 
                    r['telephone'] or "", 
                    r['adresse'] or ""
                ))
            self.info_label.configure(text=f"📊 {len(rows)} client(s) trouvé(s)")
        else:
            self.info_label.configure(text="📊 Aucun client trouvé")

    def search(self):
        """Recherche des clients via le contrôleur"""
        term = self.search_var.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if term:
            rows = self.controller.search_clients_by_nom(term)
        else:
            rows = self.controller.get_all_clients()
        
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(
                    r['id'], 
                    r['nom'], 
                    r['email'], 
                    r['telephone'] or "", 
                    r['adresse'] or ""
                ))
            self.info_label.configure(text=f"📊 {len(rows)} résultat(s) trouvé(s)")
        else:
            self.info_label.configure(text="📊 Aucun résultat trouvé")

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
        win.geometry("480x500")
        win.resizable(False, False)
        win.grab_set()
        
        # Centrer la fenêtre
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (480 // 2)
        y = (win.winfo_screenheight() // 2) - (500 // 2)
        win.geometry(f"480x500+{x}+{y}")

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

        # Titre
        title_text = "Modifier un client" if client_id else "Ajouter un client"
        ctk.CTkLabel(
            win, 
            text=title_text, 
            font=("Arial", 20, "bold"),
            text_color="#e67e22"
        ).pack(pady=(20, 20))

        # Frame pour le formulaire
        form_frame = ctk.CTkFrame(win, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")

        # Champ Nom
        ctk.CTkLabel(form_frame, text="Nom complet :", font=("Arial", 13)).grid(row=0, column=0, padx=5, pady=12, sticky="e")
        entry_nom = ctk.CTkEntry(form_frame, textvariable=nom_var, width=280, placeholder_text="Ex: Jean Dupont")
        entry_nom.grid(row=0, column=1, padx=5, pady=12)

        # Champ Email
        ctk.CTkLabel(form_frame, text="Email :", font=("Arial", 13)).grid(row=1, column=0, padx=5, pady=12, sticky="e")
        entry_email = ctk.CTkEntry(form_frame, textvariable=email_var, width=280, placeholder_text="Ex: jean@example.com")
        entry_email.grid(row=1, column=1, padx=5, pady=12)

        # Champ Téléphone
        ctk.CTkLabel(form_frame, text="Téléphone :", font=("Arial", 13)).grid(row=2, column=0, padx=5, pady=12, sticky="e")
        entry_telephone = ctk.CTkEntry(form_frame, textvariable=telephone_var, width=280, placeholder_text="Ex: 06 12 34 56 78")
        entry_telephone.grid(row=2, column=1, padx=5, pady=12)

        # Champ Adresse
        ctk.CTkLabel(form_frame, text="Adresse :", font=("Arial", 13)).grid(row=3, column=0, padx=5, pady=12, sticky="e")
        entry_adresse = ctk.CTkEntry(form_frame, textvariable=adresse_var, width=280, placeholder_text="Ex: 10 rue de Paris, 75001 Paris")
        entry_adresse.grid(row=3, column=1, padx=5, pady=12)

        def save():
            # Récupération des valeurs
            nom = entry_nom.get().strip()
            email = entry_email.get().strip()
            telephone = entry_telephone.get().strip()
            adresse = entry_adresse.get().strip()

            # Validation du nom via le contrôleur
            is_valid, error_msg = self.controller.validate_nom(nom)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_nom.focus()
                return

            # Validation de l'email via le contrôleur
            is_valid, error_msg = self.controller.validate_email(email)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_email.focus()
                return

            # Vérification doublon email via le contrôleur
            if self.controller.check_email_exists(email, client_id):
                messagebox.showerror("Erreur", "Cet email est déjà utilisé par un autre client.")
                entry_email.focus()
                return

            # Formatage du téléphone
            telephone = self.controller.format_telephone(telephone)
            adresse = adresse if adresse else None

            # Enregistrement via le contrôleur
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
            fg_color="#e67e22", 
            hover_color="#d35400", 
            corner_radius=10,
            width=200,
            height=40,
            font=("Arial", 14, "bold")
        ).pack(pady=25)

        # Mettre le focus sur le premier champ
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
        messagebox.showinfo("Export", f"Exporté vers : {filename}")
    
    
    
    
    
    
    
    
    
    
    
    
    