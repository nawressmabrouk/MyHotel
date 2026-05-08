# controllers/chambres_controller.py
import database as db

class ChambresController:
    """Contrôleur pour la gestion des chambres"""
    
    @staticmethod
    def get_all_chambres():
        """Récupère toutes les chambres"""
        query = "SELECT id, numero, type, prix_nuit, statut FROM chambres ORDER BY numero"
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def search_chambres_by_numero(search_term):
        """Recherche des chambres par numéro"""
        query = "SELECT id, numero, type, prix_nuit, statut FROM chambres WHERE numero LIKE %s ORDER BY numero"
        return db.execute_query(query, (f"%{search_term}%",), fetch=True)
    
    @staticmethod
    def get_chambre_by_id(chambre_id):
        """Récupère une chambre par son ID"""
        query = "SELECT id, numero, type, prix_nuit, statut FROM chambres WHERE id = %s"
        return db.execute_query(query, (chambre_id,), fetch_one=True)
    
    @staticmethod
    def get_chambre_for_form(chambre_id):
        """Récupère les données d'une chambre pour le formulaire"""
        query = "SELECT numero, type, prix_nuit, statut FROM chambres WHERE id = %s"
        return db.execute_query(query, (chambre_id,), fetch_one=True)
    
    @staticmethod
    def add_chambre(numero, chambre_type, prix_nuit, statut):
        """Ajoute une nouvelle chambre"""
        query = """INSERT INTO chambres (numero, type, prix_nuit, statut) 
                   VALUES (%s, %s, %s, %s)"""
        return db.execute_query(query, (numero, chambre_type, prix_nuit, statut))
    
    @staticmethod
    def update_chambre(chambre_id, numero, chambre_type, prix_nuit, statut):
        """Modifie une chambre existante"""
        query = """UPDATE chambres 
                   SET numero=%s, type=%s, prix_nuit=%s, statut=%s 
                   WHERE id=%s"""
        return db.execute_query(query, (numero, chambre_type, prix_nuit, statut, chambre_id))
    
    @staticmethod
    def delete_chambre(chambre_id):
        """Supprime une chambre"""
        return db.execute_query("DELETE FROM chambres WHERE id = %s", (chambre_id,))
    
    @staticmethod
    def validate_price(prix):
        """Valide le prix"""
        try:
            prix_float = float(prix)
            if prix_float <= 0:
                raise ValueError
            return prix_float, True, ""
        except ValueError:
            return None, False, "Le prix doit être un nombre positif (ex: 50.00)"
    
    @staticmethod
    def check_numero_exists(numero, exclude_id=None):
        """Vérifie si un numéro de chambre existe déjà"""
        if exclude_id:
            query = "SELECT id FROM chambres WHERE numero = %s AND id != %s"
            result = db.execute_query(query, (numero, exclude_id), fetch_one=True)
        else:
            query = "SELECT id FROM chambres WHERE numero = %s"
            result = db.execute_query(query, (numero,), fetch_one=True)
        return result is not None