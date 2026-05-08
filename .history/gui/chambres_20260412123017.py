# gui/chambres.py
from fileinput import filename
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import customtkinter as ctk
from tkinter import filedialog, ttk, messagebox
import csv
from controllers.chambres_controller import ChambresController

class ChambresFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = ChambresController()  
        self.create_widgets()
        self.load_data()
        self.pack(fill="both", expand=True)

    def create_widgets(self):
        # Style pour le Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # === FRAME POUR LE TABLEAU ===
        table_container = ctk.CTkFrame(
            self, 
            corner_radius=15,
            border_width=2,
            border_color="#e67e22",
            fg_color="transparent"
        )
        table_container.pack(fill="both", expand=True, padx=15, pady=15)

        # === CRÉATION DU TREEVIEW ===
        columns = ("id", "numero", "type", "prix_nuit", "statut")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=18)
        
        column_configs = {
            "id": {"text": "ID", "width": 50, "anchor": "center"},
            "numero": {"text": "Numéro", "width": 100, "anchor": "center"},
            "type": {"text": "Type", "width": 120, "anchor": "center"},
            "prix_nuit": {"text": "Prix/nuit (€)", "width": 120, "anchor": "e"},
            "statut": {"text": "Statut", "width": 120, "anchor": "center"}
        }
        
        for col, config in column_configs.items():
            self.tree.heading(col, text=config["text"])
            self.tree.column(col, width=config["width"], anchor=config["anchor"])

        # Scrollbars
        v_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # === FRAME DES BOUTONS ===
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

        # === BARRE DE RECHERCHE ===
        search_frame = ctk.CTkFrame(btn_container, fg_color="transparent")
        search_frame.pack(pady=10)

        ctk.CTkLabel(
            search_frame, 
            text="🔍 Rechercher par numéro :", 
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
            placeholder_text="Numéro de chambre..."
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

        # === INFO BAR ===
        self.info_label = ctk.CTkLabel(
            btn_container,
            text="",
            font=("Arial", 11),
            text_color="gray"
        )
        self.info_label.pack(pady=5)

    def load_data(self):
        """Charge toutes les chambres via le contrôleur"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        rows = self.controller.get_all_chambres()
        
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(
                    r['id'], 
                    r['numero'], 
                    r['type'], 
                    f"{r['prix_nuit']:.2f}", 
                    r['statut']
                ))
            self.info_label.configure(text=f"📊 {len(rows)} chambre(s) trouvée(s)")
        else:
            self.info_label.configure(text="📊 Aucune chambre trouvée")

    def search(self):
        """Recherche des chambres via le contrôleur"""
        num = self.search_var.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if num:
            rows = self.controller.search_chambres_by_numero(num)
        else:
            rows = self.controller.get_all_chambres()
        
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(
                    r['id'], 
                    r['numero'], 
                    r['type'], 
                    f"{r['prix_nuit']:.2f}", 
                    r['statut']
                ))
            self.info_label.configure(text=f"📊 {len(rows)} résultat(s) trouvé(s)")
        else:
            self.info_label.configure(text="📊 Aucun résultat trouvé")

    def add(self):
        self.open_form()

    def edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une chambre.")
            return
        item = self.tree.item(selected[0])
        chambre_id = item['values'][0]
        self.open_form(chambre_id)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une chambre.")
            return
        
        if messagebox.askyesno("Confirmation", "Supprimer cette chambre ?"):
            item = self.tree.item(selected[0])
            chambre_id = item['values'][0]
            self.controller.delete_chambre(chambre_id)
            self.load_data()
            messagebox.showinfo("Succès", "Chambre supprimée avec succès !")

    def open_form(self, chambre_id=None):
        """Ouvre le formulaire d'ajout/modification"""
        win = ctk.CTkToplevel(self)
        win.title("Ajouter / Modifier une chambre")
        win.geometry("420x450")
        win.resizable(False, False)
        win.grab_set()
        
        # Centrer la fenêtre
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (420 // 2)
        y = (win.winfo_screenheight() // 2) - (450 // 2)
        win.geometry(f"420x450+{x}+{y}")

        # Variables
        numero_var = ctk.StringVar()
        type_var = ctk.StringVar(value="simple")
        prix_var = ctk.StringVar()
        statut_var = ctk.StringVar(value="libre")

        # Si modification, charger les données via le contrôleur
        if chambre_id:
            row = self.controller.get_chambre_for_form(chambre_id)
            if row:
                numero_var.set(row['numero'])
                type_var.set(row['type'])
                prix_var.set(str(row['prix_nuit']))
                statut_var.set(row['statut'])

        # Titre
        title_text = "Modifier une chambre" if chambre_id else "Ajouter une chambre"
        ctk.CTkLabel(
            win, 
            text=title_text, 
            font=("Arial", 20, "bold"),
            text_color="#e67e22"
        ).pack(pady=(20, 20))

        # Frame pour le formulaire
        form_frame = ctk.CTkFrame(win, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")

        # Champ Numéro
        ctk.CTkLabel(form_frame, text="Numéro de chambre :", font=("Arial", 13)).grid(row=0, column=0, padx=5, pady=12, sticky="e")
        entry_numero = ctk.CTkEntry(form_frame, textvariable=numero_var, width=200, placeholder_text="Ex: 101")
        entry_numero.grid(row=0, column=1, padx=5, pady=12)

        # Champ Type
        ctk.CTkLabel(form_frame, text="Type :", font=("Arial", 13)).grid(row=1, column=0, padx=5, pady=12, sticky="e")
        ctk.CTkComboBox(form_frame, values=["simple", "double", "suite"], variable=type_var, width=200).grid(row=1, column=1, padx=5, pady=12)

        # Champ Prix
        ctk.CTkLabel(form_frame, text="Prix par nuit (€) :", font=("Arial", 13)).grid(row=2, column=0, padx=5, pady=12, sticky="e")
        entry_prix = ctk.CTkEntry(form_frame, textvariable=prix_var, width=200, placeholder_text="Ex: 50")
        entry_prix.grid(row=2, column=1, padx=5, pady=12)

        # Champ Statut
        ctk.CTkLabel(form_frame, text="Statut :", font=("Arial", 13)).grid(row=3, column=0, padx=5, pady=12, sticky="e")
        ctk.CTkComboBox(form_frame, values=["libre", "occupee", "nettoyage"], variable=statut_var, width=200).grid(row=3, column=1, padx=5, pady=12)

        def save():
            # Récupération des valeurs
            numero = entry_numero.get().strip()
            prix = entry_prix.get().strip()
            chambre_type = type_var.get()
            statut = statut_var.get()

            # Validation
            if not numero:
                messagebox.showerror("Erreur", "Le numéro de chambre est obligatoire.")
                entry_numero.focus()
                return

            if not prix:
                messagebox.showerror("Erreur", "Le prix est obligatoire.")
                entry_prix.focus()
                return

            # Validation du prix via le contrôleur
            prix_float, is_valid, error_msg = self.controller.validate_price(prix)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_prix.focus()
                return

            # Vérification doublon via le contrôleur
            if self.controller.check_numero_exists(numero, chambre_id):
                messagebox.showerror("Erreur", "Ce numéro de chambre existe déjà !")
                entry_numero.focus()
                return

            # Enregistrement via le contrôleur
            if chambre_id:
                result = self.controller.update_chambre(chambre_id, numero, chambre_type, prix_float, statut)
            else:
                result = self.controller.add_chambre(numero, chambre_type, prix_float, statut)

            if result is not None:
                win.destroy()
                self.load_data()
                messagebox.showinfo("Succès", "Chambre enregistrée avec succès !")
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
        entry_numero.focus()
    def export_csv(self):
        data = []
        for child in self.tree.get_children():
            values = self.tree.item(child)['values']
            data.append(values)
    
        if not data:
            messagebox.showwarning("Export", "Aucune donnée à exporter.")
            return
    
        # Ouvrir une boîte de dialogue pour choisir l'emplacement
        filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialfile="chambres.csv",
        title="Enregistrer le fichier CSV"
        )
    
        if filename:  # Si l'utilisateur n'a pas annulé
            with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Numéro", "Type", "Prix/nuit", "Statut"])
            writer.writerows(data)
        messagebox.showinfo("Export", f"Exporté vers : {filename}")