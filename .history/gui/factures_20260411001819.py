import customtkinter as ctk
from tkinter import ttk, messagebox
import database as db
import csv
from datetime import date
from gui.styles import configure_treeview_styles, apply_alternate_colors

class FacturesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.style = configure_treeview_styles()
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # === FRAME POUR LE TABLEAU AVEC OMBRE ===
        table_container = ctk.CTkFrame(
            self, 
            corner_radius=15,
            border_width=2,
            border_color="#e67e22",
            fg_color="transparent"
        )
        table_container.pack(fill="both", expand=True, padx=15, pady=15)

        # === FRAME INTERNE POUR LE TABLEAU ===
        inner_frame = ctk.CTkFrame(table_container, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # === CRÉATION DU TREEVIEW AVEC STYLE ===
        columns = ("id", "reservation_id", "client_nom", "chambre_numero", 
                   "montant_total", "date_paiement", "mode_paiement")
        
        self.tree = ttk.Treeview(
            inner_frame, 
            columns=columns, 
            show="headings",
            style="Custom.Treeview",
            height=18,
            selectmode="browse"
        )
        
        # Configuration des colonnes avec meilleurs titres et largeurs
        column_configs = {
            "id": {"text": "🆔 ID", "width": 60, "anchor": "center"},
            "reservation_id": {"text": "📋 Réservation", "width": 110, "anchor": "center"},
            "client_nom": {"text": "👤 Client", "width": 200, "anchor": "w"},
            "chambre_numero": {"text": "🛏️ Chambre", "width": 90, "anchor": "center"},
            "montant_total": {"text": "💰 Montant (€)", "width": 130, "anchor": "e"},
            "date_paiement": {"text": "📅 Date paiement", "width": 130, "anchor": "center"},
            "mode_paiement": {"text": "💳 Mode paiement", "width": 150, "anchor": "center"}
        }
        
        for col, config in column_configs.items():
            self.tree.heading(col, text=config["text"])
            self.tree.column(col, width=config["width"], anchor=config["anchor"])
            
            # Ajouter un tri par clic sur l'en-tête (optionnel)
            self.tree.heading(col, command=lambda c=col: self.sort_column(c, False))

        # Scrollbars stylisées
        v_scroll = ttk.Scrollbar(
            inner_frame, 
            orient="vertical", 
            command=self.tree.yview,
            style="Custom.Vertical.TScrollbar"
        )
        h_scroll = ttk.Scrollbar(
            inner_frame, 
            orient="horizontal", 
            command=self.tree.xview
        )
        
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Placement avec grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        inner_frame.grid_rowconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(0, weight=1)

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
            font=("Arial", 12),
            text_color="gray"
        )
        self.info_label.pack(pady=5)

    def sort_column(self, col, reverse):
        """Trie le tableau par colonne"""
        data_list = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data_list.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(data_list):
            self.tree.move(child, '', index)
        
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

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
            for i, r in enumerate(rows):
                # Alternance des couleurs
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                self.tree.insert("", "end", values=(
                    r['id'], r['reservation_id'], r['client_nom'], r['chambre_numero'],
                    f"{r['montant_total']:.2f}", r['date_paiement'] or "", r['mode_paiement'] or ""
                ), tags=(tag,))
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
            for i, r in enumerate(rows):
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                self.tree.insert("", "end", values=(
                    r['id'], r['reservation_id'], r['client_nom'], r['chambre_numero'],
                    f"{r['montant_total']:.2f}", r['date_paiement'] or "", r['mode_paiement'] or ""
                ), tags=(tag,))
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
        # ... (le formulaire reste identique à la version précédente)
        pass

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