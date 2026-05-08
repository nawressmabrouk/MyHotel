# controllers/dashboard_controller.py
import database as db
from datetime import datetime, timedelta

class DashboardController:
    """Contrôleur pour les statistiques et le tableau de bord"""
    
    @staticmethod
    def get_total_chambres():
        """Récupère le nombre total de chambres"""
        result = db.execute_query("SELECT COUNT(*) as total FROM chambres", fetch_one=True)
        return result['total'] if result else 0
    
    @staticmethod
    def get_chambres_libres():
        """Récupère le nombre de chambres libres"""
        result = db.execute_query(
            "SELECT COUNT(*) as total FROM chambres WHERE statut = 'libre'", 
            fetch_one=True
        )
        return result['total'] if result else 0
    
    @staticmethod
    def get_chambres_occupees():
        """Récupère le nombre de chambres occupées"""
        result = db.execute_query(
            "SELECT COUNT(*) as total FROM chambres WHERE statut = 'occupee'", 
            fetch_one=True
        )
        return result['total'] if result else 0
    
    @staticmethod
    def get_chambres_nettoyage():
        """Récupère le nombre de chambres en nettoyage"""
        result = db.execute_query(
            "SELECT COUNT(*) as total FROM chambres WHERE statut = 'nettoyage'", 
            fetch_one=True
        )
        return result['total'] if result else 0
    
    @staticmethod
    def get_total_clients():
        """Récupère le nombre total de clients"""
        result = db.execute_query("SELECT COUNT(*) as total FROM clients", fetch_one=True)
        return result['total'] if result else 0
    
    @staticmethod
    def get_reservations_actives():
        """Récupère le nombre de réservations actives"""
        result = db.execute_query(
            "SELECT COUNT(*) as total FROM reservations WHERE statut = 'active'", 
            fetch_one=True
        )
        return result['total'] if result else 0
    
    @staticmethod
    def get_reservations_total():
        """Récupère le nombre total de réservations"""
        result = db.execute_query("SELECT COUNT(*) as total FROM reservations", fetch_one=True)
        return result['total'] if result else 0
    
    @staticmethod
    def get_chiffre_affaires_total():
        """Récupère le chiffre d'affaires total (somme des montants des factures)"""
        result = db.execute_query("SELECT SUM(montant_total) as total FROM factures", fetch_one=True)
        return result['total'] if result and result['total'] else 0
    
    @staticmethod
    def get_chiffre_affaires_mois():
        """Récupère le chiffre d'affaires du mois en cours (version MySQL)"""
        result = db.execute_query("""
            SELECT SUM(montant_total) as total 
            FROM factures 
            WHERE YEAR(date_paiement) = YEAR(CURDATE()) 
            AND MONTH(date_paiement) = MONTH(CURDATE())
        """, fetch_one=True)
        return result['total'] if result and result['total'] else 0
    
    @staticmethod
    def get_reservations_recentes(limit=5):
        """Récupère les dernières réservations"""
        query = """
            SELECT r.id, c.nom as client_nom, ch.numero as chambre_numero,
                   r.date_arrivee, r.date_depart, r.statut
            FROM reservations r
            JOIN clients c ON r.client_id = c.id
            JOIN chambres ch ON r.chambre_id = ch.id
            ORDER BY r.date_arrivee DESC
            LIMIT %s
        """
        return db.execute_query(query, (limit,), fetch=True) or []
    
    @staticmethod
    def get_factures_recentes(limit=5):
        """Récupère les dernières factures"""
        query = """
            SELECT f.id, c.nom as client_nom, f.montant_total, f.date_paiement, f.mode_paiement
            FROM factures f
            JOIN reservations r ON f.reservation_id = r.id
            JOIN clients c ON r.client_id = c.id
            ORDER BY f.id DESC
            LIMIT %s
        """
        return db.execute_query(query, (limit,), fetch=True) or []
    
    @staticmethod
    def get_occupation_par_type():
        """Récupère le nombre de chambres par type et leur statut"""
        query = """
            SELECT type, statut, COUNT(*) as count
            FROM chambres
            GROUP BY type, statut
            ORDER BY type
        """
        rows = db.execute_query(query, fetch=True) or []
        
        # Formater les données pour l'affichage
        result = {}
        for row in rows:
            if row['type'] not in result:
                result[row['type']] = {'libre': 0, 'occupee': 0, 'nettoyage': 0}
            result[row['type']][row['statut']] = row['count']
        return result
    
    @staticmethod
    def get_repartition_chambres():
        """Récupère la répartition des chambres par statut"""
        query = """
            SELECT statut, COUNT(*) as count
            FROM chambres
            GROUP BY statut
        """
        rows = db.execute_query(query, fetch=True) or []
        return {row['statut']: row['count'] for row in rows}
    
    @staticmethod
    def get_ca_par_mois(months=6):
        """Récupère le chiffre d'affaires des derniers mois (version MySQL)"""
        result = []
        
        query = """
            SELECT 
                DATE_FORMAT(date_paiement, '%%b %%Y') as mois,
                SUM(montant_total) as total
            FROM factures 
            WHERE date_paiement >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
            GROUP BY YEAR(date_paiement), MONTH(date_paiement)
            ORDER BY YEAR(date_paiement), MONTH(date_paiement)
        """
        
        rows = db.execute_query(query, (months,), fetch=True) or []
        
        # Créer un dictionnaire des résultats
        ca_dict = {row['mois']: row['total'] for row in rows}
        
        # Générer tous les mois demandés
        current_date = datetime.now()
        for i in range(months - 1, -1, -1):
            month_date = current_date - timedelta(days=30 * i)
            month_name = month_date.strftime('%b %Y')
            
            result.append({
                'mois': month_name,
                'ca': ca_dict.get(month_name, 0)
            })
        
        return result
    
    @staticmethod
    def get_taux_occupation():
        """Calcule le taux d'occupation actuel"""
        total = DashboardController.get_total_chambres()
        occupees = DashboardController.get_chambres_occupees()
        
        if total == 0:
            return 0
        return round((occupees / total) * 100, 1)
    
    @staticmethod
    def get_statuts_cards():
        """Retourne toutes les statistiques pour les cartes du dashboard"""
        return {
            'total_chambres': DashboardController.get_total_chambres(),
            'chambres_libres': DashboardController.get_chambres_libres(),
            'chambres_occupees': DashboardController.get_chambres_occupees(),
            'chambres_nettoyage': DashboardController.get_chambres_nettoyage(),
            'total_clients': DashboardController.get_total_clients(),
            'reservations_actives': DashboardController.get_reservations_actives(),
            'reservations_total': DashboardController.get_reservations_total(),
            'ca_total': DashboardController.get_chiffre_affaires_total(),
            'ca_mois': DashboardController.get_chiffre_affaires_mois(),
            'taux_occupation': DashboardController.get_taux_occupation()
        }