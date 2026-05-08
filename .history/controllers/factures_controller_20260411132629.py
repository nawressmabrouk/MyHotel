# controllers/factures_controller.py
import database as db
from datetime import datetime, date

class FacturesController:
    """Contrôleur pour la gestion des factures"""
    
    @staticmethod
    def get_all_factures():
        """Récupère toutes les factures avec les infos client et chambre"""
        query = """
            SELECT f.id, f.reservation_id, c.nom as client_nom, ch.numero as chambre_numero,
                   f.montant_total, f.date_paiement, f.mode_paiement
            FROM factures f
            JOIN reservations r ON f.reservation_id = r.id
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            ORDER BY f.id DESC
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def search_factures_by_client(search_term):
        """Recherche des factures par nom de client"""
        query = """
            SELECT f.id, f.reservation_id, c.nom as client_nom, ch.numero as chambre_numero,
                   f.montant_total, f.date_paiement, f.mode_paiement
            FROM factures f
            JOIN reservations r ON f.reservation_id = r.id
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            WHERE c.nom LIKE %s
            ORDER BY f.id DESC
        """
        return db.execute_query(query, (f"%{search_term}%",), fetch=True)
    
    @staticmethod
    def get_facture_by_id(facture_id):
        """Récupère une facture par son ID"""
        query = "SELECT id, reservation_id, montant_total, date_paiement, mode_paiement FROM factures WHERE id = %s"
        return db.execute_query(query, (facture_id,), fetch_one=True)
    
    @staticmethod
    def get_reservations_sans_facture():
        """Récupère les réservations qui n'ont pas encore de facture"""
        query = """
            SELECT r.id, c.nom as client_nom, ch.numero as chambre_numero,
                   r.date_arrivee, r.date_depart
            FROM reservations r
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            WHERE r.id NOT IN (SELECT reservation_id FROM factures)
            ORDER BY r.date_arrivee
        """
        return db.execute_query(query, fetch=True) or []
    
    @staticmethod
    def get_reservation_by_id(reservation_id):
        """Récupère une réservation spécifique avec ses détails"""
        query = """
            SELECT r.id, c.nom as client_nom, ch.numero as chambre_numero,
                   r.date_arrivee, r.date_depart, ch.prix_nuit
            FROM reservations r
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            WHERE r.id = %s
        """
        return db.execute_query(query, (reservation_id,), fetch_one=True)
    
    @staticmethod
    def calculer_montant_reservation(reservation_id):
        """Calcule le montant total d'une réservation basé sur les nuits et le prix de la chambre"""
        row = db.execute_query("""
            SELECT r.date_arrivee, r.date_depart, ch.prix_nuit
            FROM reservations r
            JOIN chambres ch ON r.chambre_id = ch.id
            WHERE r.id = %s
        """, (reservation_id,), fetch_one=True)
        
        if row and row['date_arrivee'] and row['date_depart']:
            d1 = datetime.strptime(str(row['date_arrivee']), '%Y-%m-%d')
            d2 = datetime.strptime(str(row['date_depart']), '%Y-%m-%d')
            delta = (d2 - d1).days
            return delta * row['prix_nuit']
        return 0
    
    @staticmethod
    def add_facture(reservation_id, montant_total, date_paiement, mode_paiement):
        """Ajoute une nouvelle facture"""
        query = """INSERT INTO factures (reservation_id, montant_total, date_paiement, mode_paiement) 
                   VALUES (%s, %s, %s, %s)"""
        return db.execute_query(query, (reservation_id, montant_total, date_paiement, mode_paiement))
    
    @staticmethod
    def update_facture(facture_id, reservation_id, montant_total, date_paiement, mode_paiement):
        """Modifie une facture existante"""
        query = """UPDATE factures 
                   SET reservation_id=%s, montant_total=%s, date_paiement=%s, mode_paiement=%s 
                   WHERE id=%s"""
        return db.execute_query(query, (reservation_id, montant_total, date_paiement, mode_paiement, facture_id))
    
    @staticmethod
    def delete_facture(facture_id):
        """Supprime une facture"""
        return db.execute_query("DELETE FROM factures WHERE id = %s", (facture_id,))
    
    @staticmethod
    def validate_montant(montant):
        """Valide le montant total"""
        try:
            montant_float = float(montant)
            if montant_float <= 0:
                return None, False, "Le montant doit être positif."
            return montant_float, True, ""
        except (ValueError, TypeError):
            return None, False, "Le montant doit être un nombre valide."
    
    @staticmethod
    def validate_date(date_str):
        """Valide le format de date AAAA-MM-JJ"""
        if not date_str:
            return True, ""  # Date optionnelle
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, ""
        except ValueError:
            return False, "Format de date invalide. Utilisez AAAA-MM-JJ (ex: 2025-04-15)."
    
    @staticmethod
    def get_today_date():
        """Retourne la date d'aujourd'hui au format AAAA-MM-JJ"""
        return str(date.today())
    
    @staticmethod
    def format_reservation_label(reservation):
        """Formate l'affichage d'une réservation pour la combobox"""
        if not reservation:
            return ""
        return f"{reservation['client_nom']} - Ch {reservation['chambre_numero']} ({reservation['date_arrivee']}→{reservation['date_depart']})"
    
    @staticmethod
    def build_reservations_dict(reservations):
        """Construit un dictionnaire {label: id} pour les réservations"""
        result = {}
        for res in reservations:
            label = FacturesController.format_reservation_label(res)
            result[label] = res['id']
        return result