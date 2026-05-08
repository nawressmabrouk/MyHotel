import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import csv

class ChambresFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Treeview
        columns = ("id", "numero", "type", "prix_nuit", "statut")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
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
        v_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Boutons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Ajouter", command=self.add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Modifier", command=self.edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Supprimer", command=self.delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Rafraîchir", command=self.load_data).pack(side=tk.LEFT, padx=5)

        # Barre de recherche (fonctionnalité avancée)
        search_frame = ttk.Frame(self)
        search_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Label(search_frame, text="Rechercher par numéro :").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="Rechercher", command=self.search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tout afficher", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = "SELECT id, numero, type, prix_nuit, statut FROM chambres ORDER BY numero"
        rows = db.execute_query(query, fetch=True)
        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=(r['id'], r['numero'], r['type'], f"{r['prix_nuit']:.2f}", r['statut']))

    def search(self):
        num = self.search_var.get().strip()
        if num:
            query = "SELECT id, numero, type, prix_nuit, statut FROM chambres WHERE numero LIKE %s"
            rows = db.execute_query(query, params=(f"%{num}%",), fetch=True)
        else:
            rows = db.execute_query("SELECT id, numero, type, prix_nuit, statut FROM chambres", fetch=True)
        for row in self.tree.get_children():
            self.tree.delete(row)
        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=(r['id'], r['numero'], r['type'], f"{r['prix_nuit']:.2f}", r['statut']))

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
        # Fenêtre popup
        win = tk.Toplevel(self)
        win.title("Ajouter/Modifier une chambre")
        win.geometry("400x300")
        win.transient(self)
        win.grab_set()

        # Variables
        numero_var = tk.StringVar()
        type_var = tk.StringVar()
        prix_var = tk.DoubleVar()
        statut_var = tk.StringVar()

        # Remplir si modification
        if chambre_id:
            query = "SELECT numero, type, prix_nuit, statut FROM chambres WHERE id = %s"
            row = db.execute_query(query, (chambre_id,), fetch_one=True)
            if row:
                numero_var.set(row['numero'])
                type_var.set(row['type'])
                prix_var.set(row['prix_nuit'])
                statut_var.set(row['statut'])

        # Champs
        ttk.Label(win, text="Numéro :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(win, textvariable=numero_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(win, text="Type :").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        type_combo = ttk.Combobox(win, textvariable=type_var, values=["simple", "double", "suite"])
        type_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(win, text="Prix par nuit :").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(win, textvariable=prix_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(win, text="Statut :").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        statut_combo = ttk.Combobox(win, textvariable=statut_var, values=["libre", "occupee", "nettoyage"])
        statut_combo.grid(row=3, column=1, padx=5, pady=5)

        def save():
            # Validation
            if not numero_var.get().strip():
                messagebox.showerror("Erreur", "Le numéro est obligatoire.")
                return
            if prix_var.get() <= 0:
                messagebox.showerror("Erreur", "Le prix doit être positif.")
                return
            if chambre_id:
                query = """UPDATE chambres SET numero=%s, type=%s, prix_nuit=%s, statut=%s
                           WHERE id=%s"""
                params = (numero_var.get(), type_var.get(), prix_var.get(), statut_var.get(), chambre_id)
            else:
                query = """INSERT INTO chambres (numero, type, prix_nuit, statut)
                           VALUES (%s, %s, %s, %s)"""
                params = (numero_var.get(), type_var.get(), prix_var.get(), statut_var.get())
            db.execute_query(query, params)
            win.destroy()
            self.load_data()

        ttk.Button(win, text="Enregistrer", command=save).grid(row=4, column=0, columnspan=2, pady=20)
        
  
  
  
  
  
  
  
  
  
  
  
  
  
  