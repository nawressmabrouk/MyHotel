import bcrypt

password = "admin123"
salt = bcrypt.gensalt()
hash_result = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
print(f"Hash généré : {hash_result}")