# controllers/reservations_controller.py
import database as db
from datetime import datetime

class ReservationsController:
    """Contrôleur pour la gestion des réservations"""
    
    @staticmethod
    def get_all_reservations():
        """Récupère toutes les réservations avec les infos client et chambre"""
        query = """
            SELECT r.id, c.nom as client_nom, ch.numero as chambre_numero,
                   r.date_arrivee, r.date_depart, r.statut
            FROM reservations r
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            ORDER BY r.date_arrivee DESC
        """
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def search_reservations(client_id=None, statut=None):
        """Recherche des réservations par client et/ou statut"""
        conditions = []
        params = []
        
        if client_id:
            conditions.append("r.client_id = %s")
            params.append(client_id)
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
        return db.execute_query(query, tuple(params), fetch=True)
    
    @staticmethod
    def get_reservation_by_id(reservation_id):
        """Récupère une réservation par son ID"""
        query = """
            SELECT r.id, r.client_id, r.chambre_id, r.date_arrivee, r.date_depart, r.statut,
                   c.nom as client_nom, ch.numero as chambre_numero
            FROM reservations r
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            WHERE r.id = %s
        """
        return db.execute_query(query, (reservation_id,), fetch_one=True)
    
    @staticmethod
    def get_reservation_for_form(reservation_id):
        """Récupère les données d'une réservation pour le formulaire"""
        query = """
            SELECT client_id, chambre_id, date_arrivee, date_depart, statut 
            FROM reservations WHERE id = %s
        """
        return db.execute_query(query, (reservation_id,), fetch_one=True)
    
    @staticmethod
    def get_all_clients():
        """Récupère tous les clients pour les combobox"""
        return db.execute_query("SELECT id, nom FROM clients ORDER BY nom", fetch=True) or []
    
    @staticmethod
    def get_all_chambres():
        """Récupère toutes les chambres pour les combobox"""
        return db.execute_query("SELECT id, numero FROM chambres ORDER BY numero", fetch=True) or []
    
    @staticmethod
    def get_chambres_libres(date_arrivee, date_depart, exclude_chambre_id=None):
        """Récupère les chambres libres sur une période donnée"""
        query = """
            SELECT id, numero FROM chambres 
            WHERE id NOT IN (
                SELECT chambre_id FROM reservations 
                WHERE statut = 'active'
                AND date_arrivee < %s AND date_depart > %s
            )
        """
        params = [date_depart, date_arrivee]
        
        if exclude_chambre_id:
            query += " AND id != %s"
            params.append(exclude_chambre_id)
        
        query += " ORDER BY numero"
        
        return db.execute_query(query, tuple(params), fetch=True) or []
    
    @staticmethod
    def check_chambre_disponible(chambre_id, date_arrivee, date_depart, exclude_reservation_id=None):
        """Vérifie si une chambre est disponible sur une période"""
        query = """
            SELECT id FROM reservations
            WHERE chambre_id = %s AND statut = 'active'
            AND date_arrivee < %s AND date_depart > %s
        """
        params = [chambre_id, date_depart, date_arrivee]
        
        if exclude_reservation_id:
            query += " AND id != %s"
            params.append(exclude_reservation_id)
        
        conflict = db.execute_query(query, tuple(params), fetch_one=True)
        return conflict is None
    
    @staticmethod
    def add_reservation(client_id, chambre_id, date_arrivee, date_depart, statut):
        """Ajoute une nouvelle réservation"""
        query = """INSERT INTO reservations (client_id, chambre_id, date_arrivee, date_depart, statut) 
                   VALUES (%s, %s, %s, %s, %s)"""
        return db.execute_query(query, (client_id, chambre_id, date_arrivee, date_depart, statut))
    
    @staticmethod
    def update_reservation(reservation_id, client_id, chambre_id, date_arrivee, date_depart, statut):
        """Modifie une réservation existante"""
        query = """UPDATE reservations 
                   SET client_id=%s, chambre_id=%s, date_arrivee=%s, date_depart=%s, statut=%s 
                   WHERE id=%s"""
        return db.execute_query(query, (client_id, chambre_id, date_arrivee, date_depart, statut, reservation_id))
    
    @staticmethod
    def delete_reservation(reservation_id):
        """Supprime une réservation (la facture liée sera supprimée via CASCADE)"""
        return db.execute_query("DELETE FROM reservations WHERE id = %s", (reservation_id,))
    
    @staticmethod
    def validate_date(date_str):
        """Valide le format de date AAAA-MM-JJ"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, ""
        except ValueError:
            return False, "Format de date invalide. Utilisez AAAA-MM-JJ (ex: 2025-04-15)."
    
    @staticmethod
    def validate_dates(date_arrivee, date_depart):
        """Valide que la date de départ est après la date d'arrivée"""
        try:
            arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d')
            depart = datetime.strptime(date_depart, '%Y-%m-%d')
            if depart <= arrivee:
                return False, "La date de départ doit être postérieure à la date d'arrivée."
            return True, ""
        except ValueError:
            return False, "Dates invalides."
    
    @staticmethod
    def get_client_dict():
        """Retourne un dictionnaire {nom: id} pour les clients"""
        clients = ReservationsController.get_all_clients()
        return {c['nom']: c['id'] for c in clients} if clients else {}
    
    @staticmethod
    def get_chambre_dict():
        """Retourne un dictionnaire {numero: id} pour les chambres"""
        chambres = ReservationsController.get_all_chambres()
        return {c['numero']: c['id'] for c in chambres} if chambres else {}