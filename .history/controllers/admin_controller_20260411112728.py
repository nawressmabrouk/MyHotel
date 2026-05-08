import bcrypt
import database as db

def verify_password(password, password_hash):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except ValueError as e:
        print(f"Erreur de vérification : {e}")
        return False

def login_admin(username, password):
    query = "SELECT id, username, password_hash FROM admins WHERE username = %s"
    result = db.execute_query(query, (username,), fetch_one=True)
    
    if not result:
        print(f"Utilisateur '{username}' non trouvé")
        return None
    
    if verify_password(password, result['password_hash']):
        return {"id": result['id'], "username": result['username']}
    else:
        print("Mot de passe incorrect")
        return None