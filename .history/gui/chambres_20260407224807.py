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
        # Frame pour le Treeview
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview (ttk, pas CTk)
        columns = ("id", "numero", "type", "prix_nuit", "statut")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("numero", text="Numéro")
        self.tree.heading("type", text="Type")
        self.tree.heading("prix_nuit", text="Prix/nuit")
        self.tree.heading("statut", text="Statut")
        self.tree.column("id", width=40)
        self.tree.column("numero", width=80)
        self.tree.column("type", width=100)
        self.tree.column("prix_nuit", width=100)
        self.tree.column("statut", width=100)

        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Frame des boutons (CTk)
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(btn_frame, text="Ajouter", command=self.add, width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Modifier", command=self.edit, width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Supprimer", command=self.delete, width=100, fg_color="red").pack(side="left", padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Rafraîchir", command=self.load_data, width=100).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Exporter CSV", command=self.export_csv, width=100).pack(side="left", padx=5, pady=5)

        # Barre de recherche
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(search_frame, text="Rechercher par numéro :").pack(side="left", padx=5)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=200)
        self.search_entry.pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Rechercher", command=self.search, width=100).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Tout afficher", command=self.load_data, width=100).pack(side="left", padx=5)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = "SELECT id, numero, type, prix_nuit, statut FROM chambres ORDER BY numero"
        rows = db.execute_query(query, fetch=True)
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(r['id'], r['numero'], r['type'], f"{r['prix_nuit']:.2f}", r['statut']))

    def search(self):
        num = self.search_var.get().strip()
        if num:
            query = "SELECT id, numero, type, prix_nuit, statut FROM chambres WHERE numero LIKE %s"
            rows = db.execute_query(query, (f"%{num}%",), fetch=True)
        else:
            rows = db.execute_query("SELECT id, numero, type, prix_nuit, statut FROM chambres", fetch=True)
        for row in self.tree.get_children():
            self.tree.delete(row)
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(r['id'], r['numero'], r['type'], f"{r['prix_nuit']:.2f}", r['statut']))

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
        win.geometry("400x350")
        win.grab_set()

        # Variables
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

        # Widgets CTk
        ctk.CTkLabel(win, text="Numéro :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=numero_var).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Type :").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        type_combo = ctk.CTkComboBox(win, values=["simple", "double", "suite"], variable=type_var)
        type_combo.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Prix par nuit :").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=prix_var).grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Statut :").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        statut_combo = ctk.CTkComboBox(win, values=["libre", "occupee", "nettoyage"], variable=statut_var)
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

        ctk.CTkButton(win, text="Enregistrer", command=save).grid(row=4, column=0, columnspan=2, pady=20)

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