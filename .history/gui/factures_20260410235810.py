import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db
import csv
from datetime import date

class FacturesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Style basique pour le Treeview
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
        columns = ("id", "reservation_id", "client_nom", "chambre_numero", 
                   "montant_total", "date_paiement", "mode_paiement")
        
        self.tree = ttk.Treeview(
            table_container, 
            columns=columns, 
            show="headings",
            height=18
        )
        
        # Configuration des colonnes
        column_configs = {
            "id": {"text": "ID", "width": 50, "anchor": "center"},
            "reservation_id": {"text": "Réservation", "width": 100, "anchor": "center"},
            "client_nom": {"text": "Client", "width": 180, "anchor": "w"},
            "chambre_numero": {"text": "Chambre", "width": 80, "anchor": "center"},
            "montant_total": {"text": "Montant (€)", "width": 120, "anchor": "e"},
            "date_paiement": {"text": "Date paiement", "width": 120, "anchor": "center"},
            "mode_paiement": {"text": "Mode paiement", "width": 130, "anchor": "center"}
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
            ("➕ Ajouter", "#2ecc71", self.add),
            ("✏️ Modifier", "#3498db", self.edit),
            ("🗑️ Supprimer", "#e74c3c", self.delete),
            ("🔄 Rafraîchir", "#f39c12", self.load_data),
            ("📎 Exporter CSV", "#9b59b6", self.export_csv)
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
            text="🔍 Rechercher par client :", 
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
                self.tree.insert("", "end", values=(
                    r['id'], r['reservation_id'], r['client_nom'], r['chambre_numero'],
                    f"{r['montant_total']:.2f}", r['date_paiement'] or "", r['mode_paiement'] or ""
                ))
            self.info_label.configure(text=f"📊 {len(rows)} facture(s) trouvée(s)")
        else:
            self.info_label.configure(text="📊 Aucune facture trouvée")

    def search(self):
        term = self.search_var.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        
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
        
        if rows:
            for r in rows:
                self.tree.insert("", "end", values=(
                    r['id'], r['reservation_id'], r['client_nom'], r['chambre_numero'],
                    f"{r['montant_total']:.2f}", r['date_paiement'] or "", r['mode_paiement'] or ""
                ))
            self.info_label.configure(text=f"📊 {len(rows)} résultat(s) trouvé(s)")
        else:
            self.info_label.configure(text="📊 Aucun résultat trouvé")

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
        win = ctk.CTkToplevel(self)
        win.title("Ajouter/Modifier une facture")
        win.geometry("550x500")
        win.grab_set()

        # Récupérer les réservations sans facture (ou celle en cours)
        if facture_id:
            fact = db.execute_query("SELECT reservation_id, montant_total, date_paiement, mode_paiement FROM factures WHERE id = %s",
                                    (facture_id,), fetch_one=True)
        else:
            fact = None

        # Liste des réservations
        if facture_id:
            res_rows = db.execute_query("""
                SELECT r.id, CONCAT(c.nom, ' - Ch ', ch.numero, ' (', r.date_arrivee, '→', r.date_depart, ')') as label
                FROM reservations r
                JOIN clients c ON r.client_id = c.id
                JOIN chambres ch ON r.chambre_id = ch.id
                WHERE r.id = %s
            """, (fact['reservation_id'],), fetch=True)
        else:
            res_rows = db.execute_query("""
                SELECT r.id, CONCAT(c.nom, ' - Ch ', ch.numero, ' (', r.date_arrivee, '→', r.date_depart, ')') as label
                FROM reservations r
                JOIN clients c ON r.client_id = c.id
                JOIN chambres ch ON r.chambre_id = ch.id
                WHERE r.id NOT IN (SELECT reservation_id FROM factures)
                ORDER BY r.date_arrivee
            """, fetch=True) or []
        
        reservations = {row['label']: row['id'] for row in res_rows}
        res_labels = list(reservations.keys())

        res_label_var = ctk.StringVar()
        montant_var = ctk.DoubleVar()
        date_paiement_var = ctk.StringVar(value=str(date.today()))
        mode_paiement_var = ctk.StringVar()

        if fact:
            label = next((l for l, rid in reservations.items() if rid == fact['reservation_id']), "")
            res_label_var.set(label)
            montant_var.set(fact['montant_total'])
            date_paiement_var.set(str(fact['date_paiement']) if fact['date_paiement'] else str(date.today()))
            mode_paiement_var.set(fact['mode_paiement'] or "")

        # Widgets
        ctk.CTkLabel(win, text="Réservation :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        res_combo = ctk.CTkComboBox(win, values=res_labels, state="readonly", width=400)
        res_combo.grid(row=0, column=1, padx=10, pady=10)
        if fact:
            res_combo.set(label)

        ctk.CTkLabel(win, text="Montant total (€) :").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        montant_entry = ctk.CTkEntry(win, textvariable=montant_var, width=200)
        montant_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(win, text="Date paiement (AAAA-MM-JJ) :").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=date_paiement_var, width=200).grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(win, text="Mode paiement :").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        mode_combo = ctk.CTkComboBox(win, values=["carte bancaire", "espèces", "virement", "chèque"], state="readonly", width=200)
        mode_combo.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        if fact and fact['mode_paiement']:
            mode_combo.set(fact['mode_paiement'])

        def update_montant_auto(*args):
            label = res_combo.get()
            if label and label in reservations:
                res_id = reservations[label]
                row = db.execute_query("""
                    SELECT r.date_arrivee, r.date_depart, ch.prix_nuit
                    FROM reservations r
                    JOIN chambres ch ON r.chambre_id = ch.id
                    WHERE r.id = %s
                """, (res_id,), fetch_one=True)
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

        ctk.CTkButton(win, text="Enregistrer", command=save).grid(row=4, column=0, columnspan=2, pady=20)

    def export_csv(self):
        data = []
        for child in self.tree.get_children():
            values = self.tree.item(child)['values']
            data.append(values)
        if not data:
            messagebox.showwarning("Export", "Aucune donnée à exporter.")
            return
        filename = "factures.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Réservation ID", "Client", "Chambre", "Montant", "Date paiement", "Mode paiement"])
            writer.writerows(data)
        messagebox.showinfo("Export", f"Exporté vers {filename}")