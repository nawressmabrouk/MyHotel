import bcrypt
import database as db

# Créer la table si elle n'existe pas (optionnel)
db.execute_query("""
    CREATE TABLE IF NOT EXISTS admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Générer un hash pour 'admin123'
password = "admin123"
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# Vérifier si l'admin existe déjà
admin = db.execute_query("SELECT id FROM admins WHERE username = 'admin'", fetch_one=True)

if admin:
    print("⚠️ L'utilisateur 'admin' existe déjà")
else:
    db.execute_query(
        "INSERT INTO admins (username, password_hash) VALUES (%s, %s)",
        ("admin", password_hash)
    )
    print("Admin créé avec succès !")
    print("Username: admin")
    print("Password: admin123")