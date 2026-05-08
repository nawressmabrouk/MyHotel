import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from datetime import date

class FacturesFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        columns = ("id", "reservation_id", "client_nom", "chambre_numero", "montant_total", "date_paiement", "mode_paiement")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("reservation_id", text="Réservation ID")
        self.tree.heading("client_nom", text="Client")
        self.tree.heading("chambre_numero", text="Chambre")
        self.tree.heading("montant_total", text="Montant (€)")
        self.tree.heading("date_paiement", text="Date paiement")
        self.tree.heading("mode_paiement", text="Mode paiement")
        self.tree.column("id", width=40)
        self.tree.column("reservation_id", width=80)
        self.tree.column("client_nom", width=150)
        self.tree.column("chambre_numero", width=80)
        self.tree.column("montant_total", width=100)
        self.tree.column("date_paiement", width=100)
        self.tree.column("mode_paiement", width=100)

        v_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Ajouter", command=self.add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Modifier", command=self.edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Supprimer", command=self.delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Rafraîchir", command=self.load_data).pack(side=tk.LEFT, padx=5)

        # Barre de recherche
        search_frame = ttk.Frame(self)
        search_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        ttk.Label(search_frame, text="Rechercher par client :").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="Rechercher", command=self.search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tout afficher", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = """
            SELECT f.id, f.reservation_id, c.nom as client_nom, ch.numero as chambre_numero,
                   f.montant_total, f.date_paiement, f.mode_paiement
            FROM factures f
            JOIN reservations r ON f.reservation_id = r.id
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            ORDER BY f.id DESC
        """
        rows = db.execute_query(query, fetch=True)
        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=(
                    r['id'], r['reservation_id'], r['client_nom'], r['chambre_numero'],
                    f"{r['montant_total']:.2f}", r['date_paiement'] or "", r['mode_paiement'] or ""
                ))

    def search(self):
        term = self.search_var.get().strip()
        if term:
            query = """
                SELECT f.id, f.reservation_id, c.nom as client_nom, ch.numero as chambre_numero,
                       f.montant_total, f.date_paiement, f.mode_paiement
                FROM factures f
                JOIN reservations r ON f.reservation_id = r.id
                JOIN clients c ON r.client_id = c.id
                JOIN chambres ch ON r.chambre_id = ch.id
                WHERE c.nom LIKE %s
            """
            rows = db.execute_query(query, (f"%{term}%",), fetch=True)
        else:
            rows = db.execute_query("""
                SELECT f.id, f.reservation_id, c.nom as client_nom, ch.numero as chambre_numero,
                       f.montant_total, f.date_paiement, f.mode_paiement
                FROM factures f
                JOIN reservations r ON f.reservation_id = r.id
                JOIN clients c ON r.client_id = c.id
                JOIN chambres ch ON r.chambre_id = ch.id
                ORDER BY f.id DESC
            """, fetch=True)
        for row in self.tree.get_children():
            self.tree.delete(row)
        if rows:
            for r in rows:
                self.tree.insert("", tk.END, values=(
                    r['id'], r['reservation_id'], r['client_nom'], r['chambre_numero'],
                    f"{r['montant_total']:.2f}", r['date_paiement'] or "", r['mode_paiement'] or ""
                ))

    def add(self):
        self.open_form()

    def edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une facture.")
            return
        item = self.tree.item(selected[0])
        facture_id = item['values'][0]
        self.open_form(facture_id)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une facture.")
            return
        if messagebox.askyesno("Confirmation", "Supprimer cette facture ?"):
            item = self.tree.item(selected[0])
            facture_id = item['values'][0]
            db.execute_query("DELETE FROM factures WHERE id = %s", (facture_id,))
            self.load_data()

    def open_form(self, facture_id=None):
        win = tk.Toplevel(self)
        win.title("Ajouter/Modifier une facture")
        win.geometry("450x350")
        win.transient(self)
        win.grab_set()

        # Récupérer les réservations sans facture (pour l'ajout) ou celle en cours
        if facture_id:
            query_fact = "SELECT reservation_id, montant_total, date_paiement, mode_paiement FROM factures WHERE id = %s"
            fact = db.execute_query(query_fact, (facture_id,), fetch_one=True)
        else:
            fact = None

        # Liste des réservations (sans facture + éventuellement celle déjà facturée si modification)
        if facture_id:
            query_res = """
                SELECT r.id, CONCAT(c.nom, ' - Ch ', ch.numero, ' (', r.date_arrivee, '→', r.date_depart, ')') as label
                FROM reservations r
                JOIN clients c ON r.client_id = c.id
                JOIN chambres ch ON r.chambre_id = ch.id
                WHERE r.id = %s
            """
            res_rows = db.execute_query(query_res, (fact['reservation_id'],), fetch=True)
        else:
            query_res = """
                SELECT r.id, CONCAT(c.nom, ' - Ch ', ch.numero, ' (', r.date_arrivee, '→', r.date_depart, ')') as label
                FROM reservations r
                JOIN clients c ON r.client_id = c.id
                JOIN chambres ch ON r.chambre_id = ch.id
                WHERE r.id NOT IN (SELECT reservation_id FROM factures)
                ORDER BY r.date_arrivee
            """
            res_rows = db.execute_query(query_res, fetch=True) or []
        reservations = {row['label']: row['id'] for row in res_rows}
        res_labels = list(reservations.keys())

        # Variables
        res_label_var = tk.StringVar()
        montant_var = tk.DoubleVar()
        date_paiement_var = tk.StringVar()
        mode_paiement_var = tk.StringVar()

        if fact:
            # Trouver le label correspondant
            label = next((l for l, rid in reservations.items() if rid == fact['reservation_id']), "")
            res_label_var.set(label)
            montant_var.set(fact['montant_total'])
            date_paiement_var.set(str(fact['date_paiement']) if fact['date_paiement'] else "")
            mode_paiement_var.set(fact['mode_paiement'] or "")

        ttk.Label(win, text="Réservation :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        res_combo = ttk.Combobox(win, values=res_labels, state="readonly", width=40)
        res_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(win, text="Montant total (€) :").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        montant_entry = ttk.Entry(win, textvariable=montant_var)
        montant_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(win, text="Date paiement (AAAA-MM-JJ) :").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(win, textvariable=date_paiement_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(win, text="Mode paiement :").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        mode_combo = ttk.Combobox(win, values=["carte bancaire", "espèces", "virement", "chèque"], state="readonly")
        mode_combo.grid(row=3, column=1, padx=5, pady=5)
        if fact:
            mode_combo.set(fact['mode_paiement'])

        def update_montant_auto(*args):
            """Optionnel : calculer automatiquement le montant à partir de la réservation sélectionnée"""
            label = res_combo.get()
            if label and label in reservations:
                res_id = reservations[label]
                # Récupérer les dates et le prix de la chambre
                query = """
                    SELECT r.date_arrivee, r.date_depart, ch.prix_nuit
                    FROM reservations r
                    JOIN chambres ch ON r.chambre_id = ch.id
                    WHERE r.id = %s
                """
                row = db.execute_query(query, (res_id,), fetch_one=True)
                if row and row['date_arrivee'] and row['date_depart']:
                    delta = (row['date_depart'] - row['date_arrivee']).days
                    montant = delta * row['prix_nuit']
                    montant_var.set(montant)

        res_combo.bind("<<ComboboxSelected>>", update_montant_auto)

        def save():
            label = res_combo.get()
            if not label or label not in reservations:
                messagebox.showerror("Erreur", "Veuillez sélectionner une réservation valide.")
                return
            if montant_var.get() <= 0:
                messagebox.showerror("Erreur", "Le montant doit être positif.")
                return
            reservation_id = reservations[label]
            if facture_id:
                query = "UPDATE factures SET reservation_id=%s, montant_total=%s, date_paiement=%s, mode_paiement=%s WHERE id=%s"
                params = (reservation_id, montant_var.get(), date_paiement_var.get() or None, mode_combo.get() or None, facture_id)
            else:
                query = "INSERT INTO factures (reservation_id, montant_total, date_paiement, mode_paiement) VALUES (%s, %s, %s, %s)"
                params = (reservation_id, montant_var.get(), date_paiement_var.get() or None, mode_combo.get() or None)
            db.execute_query(query, params)
            win.destroy()
            self.load_data()

        ttk.Button(win, text="Enregistrer", command=save).grid(row=4, column=0, columnspan=2, pady=20)