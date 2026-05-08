import bcrypt
import database as db

def verify_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def login_admin(username, password):
    query = "SELECT id, username, password_hash FROM admins WHERE username = %s"
    result = db.execute_query(query, (username,), fetch_one=True)
    
    if result and verify_password(password, result['password_hash']):
        return {"id": result['id'], "username": result['username']}
    return None