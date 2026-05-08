import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db
import csv

class ChambresFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_data()

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
            ("➕ Ajouter", "#1a1a2e", self.add),
            ("✏️ Modifier", "#1a1a2e", self.edit),
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
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = "SELECT id, numero, type, prix_nuit, statut FROM chambres ORDER BY numero"
        rows = db.execute_query(query, fetch=True)
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(r['id'], r['numero'], r['type'], f"{r['prix_nuit']:.2f}", r['statut']))
            self.info_label.configure(text=f"📊 {len(rows)} chambre(s) trouvée(s)")
        else:
            self.info_label.configure(text="📊 Aucune chambre trouvée")

    def search(self):
        num = self.search_var.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        if num:
            query = "SELECT id, numero, type, prix_nuit, statut FROM chambres WHERE numero LIKE %s"
            rows = db.execute_query(query, (f"%{num}%",), fetch=True)
        else:
            rows = db.execute_query("SELECT id, numero, type, prix_nuit, statut FROM chambres", fetch=True)
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(r['id'], r['numero'], r['type'], f"{r['prix_nuit']:.2f}", r['statut']))
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
        if messagebox.askyesno("Confirmation", "Supprimer cette chambre ? Les réservations liées seront aussi supprimées."):
            item = self.tree.item(selected[0])
            chambre_id = item['values'][0]
            db.execute_query("DELETE FROM chambres WHERE id = %s", (chambre_id,))
            self.load_data()

    def open_form(self, chambre_id=None):
        win = ctk.CTkToplevel(self)
        win.title("Ajouter/Modifier une chambre")
        win.geometry("400x380")
        win.grab_set()

        numero_var = ctk.StringVar()
        type_var = ctk.StringVar()
        prix_var = ctk.DoubleVar()
        statut_var = ctk.StringVar()

        if chambre_id:
            query = "SELECT numero, type, prix_nuit, statut FROM chambres WHERE id = %s"
            row = db.execute_query(query, (chambre_id,), fetch_one=True)
            if row:
                numero_var.set(row['numero'])
                type_var.set(row['type'])
                prix_var.set(row['prix_nuit'])
                statut_var.set(row['statut'])

        ctk.CTkLabel(win, text="Numéro :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=numero_var, width=200).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Type :").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        type_combo = ctk.CTkComboBox(win, values=["simple", "double", "suite"], variable=type_var, width=200)
        type_combo.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Prix par nuit (€) :").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=prix_var, width=200).grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Statut :").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        statut_combo = ctk.CTkComboBox(win, values=["libre", "occupee", "nettoyage"], variable=statut_var, width=200)
        statut_combo.grid(row=3, column=1, padx=10, pady=10)

        def save():
            if not numero_var.get().strip():
                messagebox.showerror("Erreur", "Le numéro est obligatoire.")
                return
            if prix_var.get() <= 0:
                messagebox.showerror("Erreur", "Le prix doit être positif.")
                return
            if chambre_id:
                query = "UPDATE chambres SET numero=%s, type=%s, prix_nuit=%s, statut=%s WHERE id=%s"
                params = (numero_var.get(), type_var.get(), prix_var.get(), statut_var.get(), chambre_id)
            else:
                query = "INSERT INTO chambres (numero, type, prix_nuit, statut) VALUES (%s, %s, %s, %s)"
                params = (numero_var.get(), type_var.get(), prix_var.get(), statut_var.get())
            db.execute_query(query, params)
            win.destroy()
            self.load_data()

        ctk.CTkButton(win, text="💾 Enregistrer", command=save, fg_color="#e67e22", hover_color="#d35400", corner_radius=10).grid(row=4, column=0, columnspan=2, pady=20)

    def export_csv(self):
        data = []
        for child in self.tree.get_children():
            values = self.tree.item(child)['values']
            data.append(values)
        if not data:
            messagebox.showwarning("Export", "Aucune donnée à exporter.")
            return
        filename = "chambres.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Numéro", "Type", "Prix/nuit", "Statut"])
            writer.writerows(data)
        messagebox.showinfo("Export", f"Exporté vers {filename}")