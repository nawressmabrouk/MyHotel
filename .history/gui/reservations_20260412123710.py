import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import customtkinter as ctk
from tkinter import filedialog, ttk, messagebox
import csv
from controllers.reservations_controller import ReservationsController

class ReservationsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = ReservationsController()
        self.client_dict = {}
        self.chambre_dict = {}
        self.create_widgets()
        self.load_data()
        self.load_client_list()
        self.pack(fill="both", expand=True)


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

        self.info_label = ctk.CTkLabel(
            btn_container,
            text="",
            font=("Arial", 11),
            text_color="gray"
        )
        self.info_label.pack(pady=5)

    def load_client_list(self):
        """Charge la liste des clients pour le filtre"""
        clients = self.controller.get_all_clients()
        self.client_dict = {c['nom']: c['id'] for c in clients} if clients else {}
        self.filter_client.configure(values=list(self.client_dict.keys()))

    def load_data(self):
        """Charge toutes les réservations via le contrôleur"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        self.filter_client.set("")
        self.filter_statut.set("")
        
        rows = self.controller.get_all_reservations()
        
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
        """Recherche des réservations via le contrôleur"""
        client_nom = self.filter_client.get()
        statut = self.filter_statut.get()
        
        client_id = self.client_dict.get(client_nom) if client_nom else None
        
        rows = self.controller.search_reservations(client_id, statut if statut else None)
        
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
            self.controller.delete_reservation(reservation_id)
            self.load_data()
            messagebox.showinfo("Succès", "Réservation supprimée avec succès !")

    def open_form(self, reservation_id=None):
        """Ouvre le formulaire d'ajout/modification"""
        win = ctk.CTkToplevel(self)
        win.title("Ajouter / Modifier une réservation")
        win.geometry("550x650")
        win.resizable(False, False)
        win.grab_set()
        
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (550 // 2)
        y = (win.winfo_screenheight() // 2) - (650 // 2)
        win.geometry(f"550x650+{x}+{y}")

        title_text = "Modifier une réservation" if reservation_id else "Ajouter une réservation"
        ctk.CTkLabel(
            win, 
            text=title_text, 
            font=("Arial", 20, "bold"),
            text_color="#e67e22"
        ).pack(pady=(20, 20))

        form_frame = ctk.CTkFrame(win, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")

        # Chargement des données via le contrôleur
        clients = self.controller.get_all_clients()
        chambres = self.controller.get_all_chambres()

        if not clients:
            messagebox.showerror("Erreur", "Aucun client trouvé. Veuillez d'abord ajouter un client.")
            win.destroy()
            return
        
        if not chambres:
            messagebox.showerror("Erreur", "Aucune chambre trouvée. Veuillez d'abord ajouter une chambre.")
            win.destroy()
            return

        client_dict = {c['nom']: c['id'] for c in clients}
        chambre_dict = {c['numero']: c['id'] for c in chambres}
        client_names = list(client_dict.keys())
        chambre_nums = list(chambre_dict.keys())

        date_arrivee_var = ctk.StringVar()
        date_depart_var = ctk.StringVar()
        statut_var = ctk.StringVar(value="active")

        client_default = ""
        chambre_default = ""
        
        if reservation_id:
            row = self.controller.get_reservation_for_form(reservation_id)
            if row:
                client_nom = next((n for n, cid in client_dict.items() if cid == row['client_id']), "")
                chambre_num = next((num for num, cid in chambre_dict.items() if cid == row['chambre_id']), "")
                client_default = client_nom
                chambre_default = chambre_num
                date_arrivee_var.set(str(row['date_arrivee']))
                date_depart_var.set(str(row['date_depart']))
                statut_var.set(row['statut'])

        ctk.CTkLabel(form_frame, text="Client :", font=("Arial", 13)).grid(row=0, column=0, padx=5, pady=12, sticky="e")
        client_combo = ctk.CTkComboBox(form_frame, values=client_names, state="readonly", width=280)
        client_combo.grid(row=0, column=1, padx=5, pady=12)
        if client_default:
            client_combo.set(client_default)
        elif client_names:
            client_combo.set(client_names[0])

        ctk.CTkLabel(form_frame, text="Chambre :", font=("Arial", 13)).grid(row=1, column=0, padx=5, pady=12, sticky="e")
        chambre_combo = ctk.CTkComboBox(form_frame, values=chambre_nums, state="readonly", width=280)
        chambre_combo.grid(row=1, column=1, padx=5, pady=12)
        if chambre_default:
            chambre_combo.set(chambre_default)
        elif chambre_nums:
            chambre_combo.set(chambre_nums[0])

        ctk.CTkLabel(form_frame, text="Date arrivée (AAAA-MM-JJ) :", font=("Arial", 13)).grid(row=2, column=0, padx=5, pady=12, sticky="e")
        entry_arrivee = ctk.CTkEntry(form_frame, textvariable=date_arrivee_var, width=280, placeholder_text="Ex: 2025-04-15")
        entry_arrivee.grid(row=2, column=1, padx=5, pady=12)

        ctk.CTkLabel(form_frame, text="Date départ (AAAA-MM-JJ) :", font=("Arial", 13)).grid(row=3, column=0, padx=5, pady=12, sticky="e")
        entry_depart = ctk.CTkEntry(form_frame, textvariable=date_depart_var, width=280, placeholder_text="Ex: 2025-04-20")
        entry_depart.grid(row=3, column=1, padx=5, pady=12)

        ctk.CTkLabel(form_frame, text="Statut :", font=("Arial", 13)).grid(row=4, column=0, padx=5, pady=12, sticky="e")
        statut_combo = ctk.CTkComboBox(form_frame, values=["active", "terminee", "annulee"], state="readonly", width=280)
        statut_combo.grid(row=4, column=1, padx=5, pady=12)
        statut_combo.set(statut_var.get())

        def save():
            client_name = client_combo.get()
            chambre_num = chambre_combo.get()
            arrivee = entry_arrivee.get().strip()
            depart = entry_depart.get().strip()
            statut = statut_combo.get()

            # Validation des champs obligatoires
            if not client_name or not chambre_num or not arrivee or not depart:
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return

            if client_name not in client_dict:
                messagebox.showerror("Erreur", "Client invalide.")
                return
            if chambre_num not in chambre_dict:
                messagebox.showerror("Erreur", "Chambre invalide.")
                return

            # Validation des dates via le contrôleur
            is_valid, error_msg = self.controller.validate_date(arrivee)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_arrivee.focus()
                return

            is_valid, error_msg = self.controller.validate_date(depart)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_depart.focus()
                return

            is_valid, error_msg = self.controller.validate_dates(arrivee, depart)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_depart.focus()
                return

            client_id = client_dict[client_name]
            chambre_id = chambre_dict[chambre_num]

            # Vérification de disponibilité via le contrôleur
            if not reservation_id:
                disponible = self.controller.check_chambre_disponible(chambre_id, arrivee, depart)
                if not disponible:
                    messagebox.showerror("Erreur", "La chambre n'est pas disponible sur cette période.")
                    return
            else:
                disponible = self.controller.check_chambre_disponible(chambre_id, arrivee, depart, reservation_id)
                if not disponible:
                    messagebox.showerror("Erreur", "La chambre n'est pas disponible sur cette période.")
                    return

            # Enregistrement via le contrôleur
            if reservation_id:
                result = self.controller.update_reservation(reservation_id, client_id, chambre_id, arrivee, depart, statut)
            else:
                result = self.controller.add_reservation(client_id, chambre_id, arrivee, depart, statut)

            if result is not None:
                win.destroy()
                self.load_data()
                self.load_client_list()
                messagebox.showinfo("Succès", "Réservation enregistrée avec succès !")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'enregistrement.")

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

        entry_arrivee.focus()
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
        initialfile="reservations.csv",
        title="Enregistrer le fichier CSV"
    )
    
    if filename:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Client", "Chambre", "Arrivée", "Départ", "Statut"])
            writer.writerows(data)
        messagebox.showinfo("Export", f"Exporté vers : {filename}")