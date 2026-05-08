import mysql.connector
from mysql.connector import Error
import config

def get_connection():
    try:
        conn = mysql.connector.connect(**config.DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erreur connexion : {e}")
        return None

def execute_query(query, params=None, fetch=False, fetch_one=False):
    """Exécute une requête.
       fetch=True retourne toutes les lignes (SELECT).
       fetch_one=True retourne une seule ligne.
    """
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        elif fetch_one:
            result = cursor.fetchone()
        else:
            conn.commit()
            result = cursor.lastrowid
        return result
    except Error as e:
        print(f"Erreur SQL : {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()