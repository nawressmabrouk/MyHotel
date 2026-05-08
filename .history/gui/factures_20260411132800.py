# gui/factures.py
import customtkinter as ctk
from tkinter import ttk, messagebox
import csv
from controllers.factures_controller import FacturesController

class FacturesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.controller = FacturesController()
        self.create_widgets()
        self.load_data()

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

        columns = ("id", "reservation_id", "client_nom", "chambre_numero", 
                   "montant_total", "date_paiement", "mode_paiement")
        
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=18)
        
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

        self.info_label = ctk.CTkLabel(
            btn_container,
            text="",
            font=("Arial", 11),
            text_color="gray"
        )
        self.info_label.pack(pady=5)

    def load_data(self):
        """Charge toutes les factures via le contrôleur"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        rows = self.controller.get_all_factures()
        
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
        """Recherche des factures via le contrôleur"""
        term = self.search_var.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if term:
            rows = self.controller.search_factures_by_client(term)
        else:
            rows = self.controller.get_all_factures()
        
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
            self.controller.delete_facture(facture_id)
            self.load_data()
            messagebox.showinfo("Succès", "Facture supprimée avec succès !")

    def open_form(self, facture_id=None):
        """Ouvre le formulaire d'ajout/modification"""
        win = ctk.CTkToplevel(self)
        win.title("Ajouter / Modifier une facture")
        win.geometry("550x550")
        win.resizable(False, False)
        win.grab_set()
        
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (550 // 2)
        y = (win.winfo_screenheight() // 2) - (550 // 2)
        win.geometry(f"550x550+{x}+{y}")

        title_text = "Modifier une facture" if facture_id else "Ajouter une facture"
        ctk.CTkLabel(
            win, 
            text=title_text, 
            font=("Arial", 20, "bold"),
            text_color="#e67e22"
        ).pack(pady=(20, 20))

        form_frame = ctk.CTkFrame(win, fg_color="transparent")
        form_frame.pack(padx=30, fill="x")

        # Récupération des données via le contrôleur
        facture = None
        if facture_id:
            facture = self.controller.get_facture_by_id(facture_id)

        # Récupération des réservations sans facture
        reservations_sans_facture = self.controller.get_reservations_sans_facture()

        if not reservations_sans_facture and not facture_id:
            messagebox.showwarning("Attention", "Aucune réservation disponible pour créer une facture.\nVeuillez d'abord créer une réservation.")
            win.destroy()
            return

        # Construction du dictionnaire des réservations
        reservations_dict = self.controller.build_reservations_dict(reservations_sans_facture)

        # Si modification, ajouter aussi la réservation actuelle de la facture
        if facture_id and facture:
            reservation_actuelle = self.controller.get_reservation_by_id(facture['reservation_id'])
            if reservation_actuelle:
                label = self.controller.format_reservation_label(reservation_actuelle)
                reservations_dict[label] = reservation_actuelle['id']

        res_labels = list(reservations_dict.keys())

        # Variables
        montant_var = ctk.DoubleVar()
        date_paiement_var = ctk.StringVar(value=self.controller.get_today_date())
        mode_paiement_var = ctk.StringVar()
        res_label_var = ctk.StringVar()

        # Chargement des valeurs si modification
        if facture_id and facture:
            for label, rid in reservations_dict.items():
                if rid == facture['reservation_id']:
                    res_label_var.set(label)
                    break
            montant_var.set(facture['montant_total'])
            date_paiement_var.set(str(facture['date_paiement']) if facture['date_paiement'] else self.controller.get_today_date())
            mode_paiement_var.set(facture['mode_paiement'] or "")

        # Widgets du formulaire
        ctk.CTkLabel(form_frame, text="Réservation :", font=("Arial", 13)).grid(row=0, column=0, padx=5, pady=12, sticky="e")
        res_combo = ctk.CTkComboBox(form_frame, values=res_labels, state="readonly", width=380)
        res_combo.grid(row=0, column=1, padx=5, pady=12)
        if res_labels:
            if res_label_var.get():
                res_combo.set(res_label_var.get())
            else:
                res_combo.set(res_labels[0])

        ctk.CTkLabel(form_frame, text="Montant total (€) :", font=("Arial", 13)).grid(row=1, column=0, padx=5, pady=12, sticky="e")
        entry_montant = ctk.CTkEntry(form_frame, textvariable=montant_var, width=200, placeholder_text="Calculé automatiquement")
        entry_montant.grid(row=1, column=1, padx=5, pady=12, sticky="w")

        ctk.CTkLabel(form_frame, text="Date paiement (AAAA-MM-JJ) :", font=("Arial", 13)).grid(row=2, column=0, padx=5, pady=12, sticky="e")
        entry_date = ctk.CTkEntry(form_frame, textvariable=date_paiement_var, width=200, placeholder_text="Ex: 2025-04-11")
        entry_date.grid(row=2, column=1, padx=5, pady=12, sticky="w")

        ctk.CTkLabel(form_frame, text="Mode paiement :", font=("Arial", 13)).grid(row=3, column=0, padx=5, pady=12, sticky="e")
        mode_combo = ctk.CTkComboBox(form_frame, values=["carte bancaire", "espèces", "virement", "chèque"], state="readonly", width=200)
        mode_combo.grid(row=3, column=1, padx=5, pady=12, sticky="w")
        if mode_paiement_var.get():
            mode_combo.set(mode_paiement_var.get())

        def update_montant_auto(*args):
            """Met à jour automatiquement le montant quand on change de réservation"""
            label = res_combo.get()
            if label and label in reservations_dict:
                res_id = reservations_dict[label]
                montant = self.controller.calculer_montant_reservation(res_id)
                montant_var.set(montant)

        res_combo.bind("<<ComboboxSelected>>", update_montant_auto)

        def save():
            label = res_combo.get()
            if not label or label not in reservations_dict:
                messagebox.showerror("Erreur", "Veuillez sélectionner une réservation valide.")
                return
            
            # Validation du montant via le contrôleur
            montant, is_valid, error_msg = self.controller.validate_montant(montant_var.get())
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_montant.focus()
                return
            
            # Validation de la date via le contrôleur
            date_paiement = entry_date.get().strip()
            is_valid, error_msg = self.controller.validate_date(date_paiement)
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                entry_date.focus()
                return

            reservation_id = reservations_dict[label]
            mode_paiement = mode_combo.get() if mode_combo.get() else None
            
            if not date_paiement:
                date_paiement = None

            # Enregistrement via le contrôleur
            if facture_id:
                result = self.controller.update_facture(facture_id, reservation_id, montant, date_paiement, mode_paiement)
            else:
                result = self.controller.add_facture(reservation_id, montant, date_paiement, mode_paiement)

            if result is not None:
                win.destroy()
                self.load_data()
                messagebox.showinfo("Succès", "Facture enregistrée avec succès !")
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

        # Calcul initial du montant
        if res_labels:
            update_montant_auto()

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