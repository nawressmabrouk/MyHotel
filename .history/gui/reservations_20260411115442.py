import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db
import csv

class ReservationsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()
        self.load_data()
        self.load_client_list()

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
        columns = ("id", "client_nom", "chambre_numero", "date_arrivee", "date_depart", "statut")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=18)
        
        column_configs = {
            "id": {"text": "ID", "width": 50, "anchor": "center"},
            "client_nom": {"text": "Client", "width": 180, "anchor": "w"},
            "chambre_numero": {"text": "Chambre", "width": 100, "anchor": "center"},
            "date_arrivee": {"text": "Arrivée", "width": 120, "anchor": "center"},
            "date_depart": {"text": "Départ", "width": 120, "anchor": "center"},
            "statut": {"text": "Statut", "width": 100, "anchor": "center"}
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
            ("🔄 Rafraîchir", "#1a1a2e", self.load_data),
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

        # === FILTRES AVANCÉS ===
        filter_frame = ctk.CTkFrame(btn_container, fg_color="transparent")
        filter_frame.pack(pady=10)

        ctk.CTkLabel(
            filter_frame, 
            text="🔍 Filtrer par :", 
            font=("Arial", 13, "bold"),
            text_color="#e67e22"
        ).pack(side="left", padx=5)

        ctk.CTkLabel(filter_frame, text="Client :", font=("Arial", 12)).pack(side="left", padx=5)
        self.filter_client = ctk.CTkComboBox(filter_frame, values=[], width=180, state="readonly")
        self.filter_client.pack(side="left", padx=5)

        ctk.CTkLabel(filter_frame, text="Statut :", font=("Arial", 12)).pack(side="left", padx=5)
        self.filter_statut = ctk.CTkComboBox(filter_frame, values=["", "active", "terminee", "annulee"], width=120, state="readonly")
        self.filter_statut.pack(side="left", padx=5)

        ctk.CTkButton(
            filter_frame, 
            text="Appliquer", 
            width=100,
            height=35,
            corner_radius=15,
            fg_color="#e67e22",
            hover_color="#d35400",
            command=self.search
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            filter_frame, 
            text="Réinitialiser", 
            width=100,
            height=35,
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

    def load_client_list(self):
        clients = db.execute_query("SELECT id, nom FROM clients ORDER BY nom", fetch=True)
        self.client_list = {c['nom']: c['id'] for c in clients} if clients else {}
        self.filter_client.configure(values=list(self.client_list.keys()))

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Réinitialiser les filtres
        self.filter_client.set("")
        self.filter_statut.set("")
        
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
                self.tree.insert("", "end", values=(
                    r['id'], r['client_nom'], r['chambre_numero'],
                    r['date_arrivee'], r['date_depart'], r['statut']
                ))
            self.info_label.configure(text=f"📊 {len(rows)} réservation(s) trouvée(s)")
        else:
            self.info_label.configure(text="📊 Aucune réservation trouvée")

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
                self.tree.insert("", "end", values=(
                    r['id'], r['client_nom'], r['chambre_numero'],
                    r['date_arrivee'], r['date_depart'], r['statut']
                ))
            self.info_label.configure(text=f"📊 {len(rows)} résultat(s) trouvé(s)")
        else:
            self.info_label.configure(text="📊 Aucun résultat trouvé")

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
        win = ctk.CTkToplevel(self)
        win.title("Ajouter/Modifier une réservation")
        win.geometry("550x550")
        win.grab_set()

        # Variables
        client_id_var = ctk.IntVar()
        chambre_id_var = ctk.IntVar()
        date_arrivee_var = ctk.StringVar()
        date_depart_var = ctk.StringVar()
        statut_var = ctk.StringVar()

        # Charger listes déroulantes
        clients = db.execute_query("SELECT id, nom FROM clients ORDER BY nom", fetch=True) or []
        chambres = db.execute_query("SELECT id, numero FROM chambres ORDER BY numero", fetch=True) or []
        client_dict = {c['nom']: c['id'] for c in clients}
        chambre_dict = {c['numero']: c['id'] for c in chambres}
        client_names = list(client_dict.keys())
        chambre_nums = list(chambre_dict.keys())

        client_default = ""
        chambre_default = ""
        if reservation_id:
            row = db.execute_query("SELECT client_id, chambre_id, date_arrivee, date_depart, statut FROM reservations WHERE id = %s",
                                   (reservation_id,), fetch_one=True)
            if row:
                client_nom = next((n for n, cid in client_dict.items() if cid == row['client_id']), "")
                chambre_num = next((num for num, cid in chambre_dict.items() if cid == row['chambre_id']), "")
                client_default = client_nom
                chambre_default = chambre_num
                date_arrivee_var.set(str(row['date_arrivee']))
                date_depart_var.set(str(row['date_depart']))
                statut_var.set(row['statut'])

        ctk.CTkLabel(win, text="Client :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        client_combo = ctk.CTkComboBox(win, values=client_names, state="readonly", width=250)
        client_combo.grid(row=0, column=1, padx=10, pady=10)
        if client_default:
            client_combo.set(client_default)

        ctk.CTkLabel(win, text="Chambre :").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        chambre_combo = ctk.CTkComboBox(win, values=chambre_nums, state="readonly", width=250)
        chambre_combo.grid(row=1, column=1, padx=10, pady=10)
        if chambre_default:
            chambre_combo.set(chambre_default)

        ctk.CTkLabel(win, text="Date arrivée (AAAA-MM-JJ) :").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=date_arrivee_var, width=250).grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Date départ (AAAA-MM-JJ) :").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(win, textvariable=date_depart_var, width=250).grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(win, text="Statut :").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        statut_combo = ctk.CTkComboBox(win, values=["active", "terminee", "annulee"], state="readonly", width=250)
        statut_combo.grid(row=4, column=1, padx=10, pady=10)
        if reservation_id:
            statut_combo.set(statut_var.get())
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

            # Vérification de disponibilité
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
                query = """UPDATE reservations SET client_id=%s, chambre_id=%s, date_arrivee=%s, date_depart=%s, statut=%s
                           WHERE id=%s"""
                params = (client_id, chambre_id, arrivee, depart, statut, reservation_id)
            else:
                query = """INSERT INTO reservations (client_id, chambre_id, date_arrivee, date_depart, statut)
                           VALUES (%s, %s, %s, %s, %s)"""
                params = (client_id, chambre_id, arrivee, depart, statut)
            db.execute_query(query, params)
            win.destroy()
            self.load_data()

        ctk.CTkButton(win, text="💾 Enregistrer", command=save, fg_color="#e67e22", hover_color="#d35400", corner_radius=10).grid(row=5, column=0, columnspan=2, pady=20)

    def export_csv(self):
        data = []
        for child in self.tree.get_children():
            values = self.tree.item(child)['values']
            data.append(values)
        if not data:
            messagebox.showwarning("Export", "Aucune donnée à exporter.")
            return
        filename = "reservations.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Client", "Chambre", "Arrivée", "Départ", "Statut"])
            writer.writerows(data)
        messagebox.showinfo("Export", f"Exporté vers {filename}")