# test_import.py
print("Test des imports...")

try:
    from gui.chambres import ChambresFrame
    print("✅ ChambresFrame importé")
except Exception as e:
    print(f"❌ Erreur ChambresFrame: {e}")

try:
    from controllers.chambres_controller import ChambresController
    print("✅ ChambresController importé")
except Exception as e:
    print(f"❌ Erreur ChambresController: {e}")

print("Test terminé !")