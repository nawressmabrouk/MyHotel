'''import bcrypt
import database as db

def hash_password(password):
    """Hash un mot de passe avec bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, password_hash):
    """Vérifie un mot de passe par rapport à son hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def login_admin(username, password):
    """Vérifie les identifiants et retourne l'admin si valide"""
    query = "SELECT id, username, password_hash FROM admins WHERE username = %s"
    result = db.execute_query(query, (username,), fetch_one=True)
    
    if result and verify_password(password, result['password_hash']):
        return {"id": result['id'], "username": result['username']}
    return None