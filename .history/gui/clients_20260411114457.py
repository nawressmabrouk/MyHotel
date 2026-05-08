import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db
import csv

class ClientsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Frame pour le Treeview
        tree_frame = ctk.CTkFrame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "nom", "email", "telephone", "adresse")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("email", text="Email")
        self.tree.heading("telephone", text="Téléphone")
        self.tree.heading("adresse", text="Adresse")
        self.tree.column("id", width=40)
        self.tree.column("nom", width=150)
        self.tree.column("email", width=180)
        self.tree.column("telephone", width=100)
        self.tree.column("adresse", width=200)

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Boutons CTk
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
        ctk.CTkLabel(search_frame, text="Rechercher par nom :").pack(side="left", padx=5)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=200)
        self.search_entry.pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Rechercher", command=self.search, width=100).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Tout afficher", command=self.load_data, width=100).pack(side="left", padx=5)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = "SELECT id, nom, email, telephone, adresse FROM clients ORDER BY nom"
        rows = db.execute_query(query, fetch=True)
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(r['id'], r['nom'], r['email'], r['telephone'], r['adresse']))

    def search(self):
        term = self.search_var.get().strip()
        if term:
            query = "SELECT id, nom, email, telephone, adresse FROM clients WHERE nom LIKE %s"
            rows = db.execute_query(query, (f"%{term}%",), fetch=True)
        else:
            rows = db.execute_query("SELECT id, nom, email, telephone, adresse FROM clients", fetch=True)
        for row in self.tree.get_children():
            self.tree.delete(row)
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(r['id'], r['nom'], r['email'], r['telephone'], r['adresse']))

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
            db.execute_query("DELETE FROM clients WHERE id = %s", (client_id,))
            self.load_data()

    def open_form(self, client_id=None):
        win = ctk.CTkToplevel(self)
        win.title("Ajouter/Modifier un client")
        win.geometry("450x400")
        win.grab_set()

        nom_var = ctk.StringVar()
        email_var = ctk.StringVar()
        telephone_var = ctk.StringVar()
        adresse_var = ctk.StringVar()

        if client_id:
            query = "SELECT nom, email, telephone, adresse FROM clients WHERE id = %s"
            row = db.execute_query(query, (client_id,), fetch_one=True)
            if row:
                nom_var.set(row['nom'])
                email_var.set(row['email'])
                telephone_var.set(row['telephone'] or '')
                adresse_var.set(row['adresse'] or '')

        ctk.CTkLabel(win, text="Nom :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=nom_var, width=250).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Email :").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=email_var, width=250).grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Téléphone :").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=telephone_var, width=250).grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Adresse :").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=adresse_var, width=250).grid(row=3, column=1, padx=10, pady=10)

        def save():
            if not nom_var.get().strip():
                messagebox.showerror("Erreur", "Le nom est obligatoire.")
                return
            if not email_var.get().strip():
                messagebox.showerror("Erreur", "L'email est obligatoire.")
                return
            if client_id:
                query = "UPDATE clients SET nom=%s, email=%s, telephone=%s, adresse=%s WHERE id=%s"
                params = (nom_var.get(), email_var.get(), telephone_var.get(), adresse_var.get(), client_id)
            else:
                query = "INSERT INTO clients (nom, email, telephone, adresse) VALUES (%s, %s, %s, %s)"
                params = (nom_var.get(), email_var.get(), telephone_var.get(), adresse_var.get())
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
        filename = "clients.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nom", "Email", "Téléphone", "Adresse"])
            writer.writerows(data)
        messagebox.showinfo("Export", f"Exporté vers {filename}")