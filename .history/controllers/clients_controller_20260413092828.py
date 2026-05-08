# controllers/clients_controller.py
import re

import database as db


class ClientsController:
    """Contrôleur pour la gestion des clients"""
    
    @staticmethod
    def get_all_clients():
        """Récupère tous les clients"""
        query = "SELECT id, nom, email, telephone, adresse FROM clients ORDER BY nom"
        return db.execute_query(query, fetch=True)
    
    @staticmethod
    def search_clients_by_nom(search_term):
        """Recherche des clients par nom"""
        query = "SELECT id, nom, email, telephone, adresse FROM clients WHERE nom LIKE %s ORDER BY nom"
        return db.execute_query(query, (f"%{search_term}%",), fetch=True)
    
    @staticmethod
    def get_client_by_id(client_id):
        """Récupère un client par son ID"""
        query = "SELECT id, nom, email, telephone, adresse FROM clients WHERE id = %s"
        return db.execute_query(query, (client_id,), fetch_one=True)
    
    @staticmethod
    def get_client_for_form(client_id):
        """Récupère les données d'un client pour le formulaire"""
        query = "SELECT nom, email, telephone, adresse FROM clients WHERE id = %s"
        return db.execute_query(query, (client_id,), fetch_one=True)
    
    @staticmethod
    def add_client(nom, email, telephone, adresse):
        """Ajoute un nouveau client"""
        query = """INSERT INTO clients (nom, email, telephone, adresse) 
                   VALUES (%s, %s, %s, %s)"""
        return db.execute_query(query, (nom, email, telephone if telephone else None, adresse if adresse else None))
    
    @staticmethod
    def update_client(client_id, nom, email, telephone, adresse):
        """Modifie un client existant"""
        query = """UPDATE clients 
                   SET nom=%s, email=%s, telephone=%s, adresse=%s 
                   WHERE id=%s"""
        return db.execute_query(query, (nom, email, telephone if telephone else None, adresse if adresse else None, client_id))
    
    @staticmethod
    def delete_client(client_id):
        """Supprime un client (les réservations seront supprimées via CASCADE)"""
        return db.execute_query("DELETE FROM clients WHERE id = %s", (client_id,))
    
    @staticmethod
    def validate_email(email):
        """Valide le format de l'email"""
        if not email:
            return False, "L'email est obligatoire."
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            return True, ""
        return False, "Veuillez entrer un email valide (ex: nom@domaine.com)."
    @staticmethod
    def validate_nom(nom):
        """Valide le nom"""
        if not isinstance(nom, str):
            return False, "Le nom doit être une chaîne de caractères."

        if not nom.strip():
            return False, "Le nom est obligatoire."

    return True, ""
    
    @staticmethod
    def check_email_exists(email, exclude_id=None):
        """Vérifie si un email existe déjà"""
        if exclude_id:
            query = "SELECT id FROM clients WHERE email = %s AND id != %s"
            result = db.execute_query(query, (email, exclude_id), fetch_one=True)
        else:
            query = "SELECT id FROM clients WHERE email = %s"
            result = db.execute_query(query, (email,), fetch_one=True)
        return result is not None
    
    @staticmethod
    def format_telephone(telephone):
        """Nettoie le numéro de téléphone (garde uniquement chiffres et espaces)"""
        if not telephone:
            return None
        # Supprime tout sauf chiffres, espaces, + et -
        cleaned = re.sub(r'[^\d\s\+\-]', '', telephone.strip())
        return cleaned if cleaned else None