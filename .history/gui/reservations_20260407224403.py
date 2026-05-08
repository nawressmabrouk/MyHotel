import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from datetime import date

class ReservationsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Treeview avec jointure pour voir client et chambre
        columns = ("id", "client_nom", "chambre_numero", "date_arrivee", "date_depart", "statut")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("client_nom", text="Client")
        self.tree.heading("chambre_numero", text="Chambre")
        self.tree.heading("date_arrivee", text="Arrivée")
        self.tree.heading("date_depart", text="Départ")
        self.tree.heading("statut", text="Statut")
        self.tree.column("id", width=40)
        self.tree.column("client_nom", width=150)
        self.tree.column("chambre_numero", width=80)
        self.tree.column("date_arrivee", width=100)
        self.tree.column("date_depart", width=100)
        self.tree.column("statut", width=80)

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

        # Filtres avancés
        filter_frame = ttk.LabelFrame(self, text="Filtrer les réservations")
        filter_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew", padx=5)
        ttk.Label(filter_frame, text="Client :").grid(row=0, column=0, padx=5, pady=2)
        self.filter_client = ttk.Combobox(filter_frame, width=20)
        self.filter_client.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(filter_frame, text="Statut :").grid(row=0, column=2, padx=5, pady=2)
        self.filter_statut = ttk.Combobox(filter_frame, values=["", "active", "terminee", "annulee"], width=10)
        self.filter_statut.grid(row=0, column=3, padx=5, pady=2)
        ttk.Button(filter_frame, text="Appliquer filtre", command=self.search).grid(row=0, column=4, padx=10, pady=2)
        ttk.Button(filter_frame, text="Réinitialiser", command=self.load_data).grid(row=0, column=5, padx=5, pady=2)

        # Charger la liste des clients pour le filtre
        self.load_client_list()

    def load_client_list(self):
        clients = db.execute_query("SELECT id, nom FROM clients ORDER BY nom", fetch=True)
        self.client_list = {c['nom']: c['id'] for c in clients} if clients else {}
        self.filter_client['values'] = list(self.client_list.keys())

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = """
            SELECT r.id, c.nom as client_nom, ch.numero as chambre_numero,
                   r.date_arrivee, r.date_depart, r.statut
            FROM reservations r
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            ORDER BY r.date_arrivee DESC
        """
        rows = db.execute_query(query, fetch=True)
        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=(
                    r['id'], r['client_nom'], r['chambre_numero'],
                    r['date_arrivee'], r['date_depart'], r['statut']
                ))

    def search(self):
        client_nom = self.filter_client.get()
        statut = self.filter_statut.get()
        conditions = []
        params = []
        if client_nom and client_nom in self.client_list:
            conditions.append("c.id = %s")
            params.append(self.client_list[client_nom])
        if statut:
            conditions.append("r.statut = %s")
            params.append(statut)
        where_clause = " AND ".join(conditions) if conditions else "1"
        query = f"""
            SELECT r.id, c.nom as client_nom, ch.numero as chambre_numero,
                   r.date_arrivee, r.date_depart, r.statut
            FROM reservations r
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            WHERE {where_clause}
            ORDER BY r.date_arrivee DESC
        """
        rows = db.execute_query(query, tuple(params), fetch=True)
        for row in self.tree.get_children():
            self.tree.delete(row)
        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=(
                    r['id'], r['client_nom'], r['chambre_numero'],
                    r['date_arrivee'], r['date_depart'], r['statut']
                ))

    def add(self):
        self.open_form()

    def edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une réservation.")
            return
        item = self.tree.item(selected[0])
        reservation_id = item['values'][0]
        self.open_form(reservation_id)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une réservation.")
            return
        if messagebox.askyesno("Confirmation", "Supprimer cette réservation ? La facture liée sera aussi supprimée."):
            item = self.tree.item(selected[0])
            reservation_id = item['values'][0]
            db.execute_query("DELETE FROM reservations WHERE id = %s", (reservation_id,))
            self.load_data()

    def open_form(self, reservation_id=None):
        win = tk.Toplevel(self)
        win.title("Ajouter/Modifier une réservation")
        win.geometry("450x400")
        win.transient(self)
        win.grab_set()

        # Variables
        client_id_var = tk.IntVar()
        chambre_id_var = tk.IntVar()
        date_arrivee_var = tk.StringVar()
        date_depart_var = tk.StringVar()
        statut_var = tk.StringVar()

        # Charger listes déroulantes
        clients = db.execute_query("SELECT id, nom FROM clients ORDER BY nom", fetch=True) or []
        chambres = db.execute_query("SELECT id, numero FROM chambres ORDER BY numero", fetch=True) or []

        client_dict = {c['nom']: c['id'] for c in clients}
        chambre_dict = {c['numero']: c['id'] for c in chambres}
        client_names = list(client_dict.keys())
        chambre_nums = list(chambre_dict.keys())

        if reservation_id:
            query = "SELECT client_id, chambre_id, date_arrivee, date_depart, statut FROM reservations WHERE id = %s"
            row = db.execute_query(query, (reservation_id,), fetch_one=True)
            if row:
                # Trouver le nom du client et le numéro de chambre
                client_nom = next((nom for nom, cid in client_dict.items() if cid == row['client_id']), "")
                chambre_num = next((num for num, cid in chambre_dict.items() if cid == row['chambre_id']), "")
                client_id_var.set(client_dict.get(client_nom, 0))
                chambre_id_var.set(chambre_dict.get(chambre_num, 0))
                date_arrivee_var.set(str(row['date_arrivee']))
                date_depart_var.set(str(row['date_depart']))
                statut_var.set(row['statut'])

        # Widgets
        ttk.Label(win, text="Client :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        client_combo = ttk.Combobox(win, values=client_names, state="readonly", width=25)
        client_combo.grid(row=0, column=1, padx=5, pady=5)
        if reservation_id and row:
            client_combo.set(client_nom)

        ttk.Label(win, text="Chambre :").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        chambre_combo = ttk.Combobox(win, values=chambre_nums, state="readonly", width=25)
        chambre_combo.grid(row=1, column=1, padx=5, pady=5)
        if reservation_id and row:
            chambre_combo.set(chambre_num)

        ttk.Label(win, text="Date arrivée (AAAA-MM-JJ) :").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(win, textvariable=date_arrivee_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(win, text="Date départ (AAAA-MM-JJ) :").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(win, textvariable=date_depart_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(win, text="Statut :").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        statut_combo = ttk.Combobox(win, values=["active", "terminee", "annulee"], state="readonly")
        statut_combo.grid(row=4, column=1, padx=5, pady=5)
        if reservation_id and row:
            statut_combo.set(row['statut'])
        else:
            statut_combo.set("active")

        def save():
            client_name = client_combo.get()
            chambre_num = chambre_combo.get()
            arrivee = date_arrivee_var.get()
            depart = date_depart_var.get()
            statut = statut_combo.get()

            if not client_name or not chambre_num or not arrivee or not depart:
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return
            if client_name not in client_dict:
                messagebox.showerror("Erreur", "Client invalide.")
                return
            if chambre_num not in chambre_dict:
                messagebox.showerror("Erreur", "Chambre invalide.")
                return

            client_id = client_dict[client_name]
            chambre_id = chambre_dict[chambre_num]

            # Vérifier disponibilité (sauf pour la réservation en cours de modification)
            query_check = """
                SELECT id FROM reservations
                WHERE chambre_id = %s
                AND id != %s
                AND statut = 'active'
                AND date_arrivee < %s
                AND date_depart > %s
            """
            params_check = (chambre_id, reservation_id or 0, depart, arrivee)
            conflict = db.execute_query(query_check, params_check, fetch_one=True)
            if conflict:
                messagebox.showerror("Erreur", "La chambre est déjà réservée sur cette période.")
                return

            if reservation_id:
                query = """UPDATE reservations
                           SET client_id=%s, chambre_id=%s, date_arrivee=%s, date_depart=%s, statut=%s
                           WHERE id=%s"""
                params = (client_id, chambre_id, arrivee, depart, statut, reservation_id)
            else:
                query = """INSERT INTO reservations (client_id, chambre_id, date_arrivee, date_depart, statut)
                           VALUES (%s, %s, %s, %s, %s)"""
                params = (client_id, chambre_id, arrivee, depart, statut)
            db.execute_query(query, params)
            win.destroy()
            self.load_data()

        ttk.Button(win, text="Enregistrer", command=save).grid(row=5, column=0, columnspan=2, pady=20)