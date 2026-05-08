# diagnostic.py
import customtkinter as ctk
from gui.chambres import ChambresFrame

def test_chambres_frame():
    print("=== DIAGNOSTIC DES CHAMBRES ===")
    
    # Créer une fenêtre de test
    root = ctk.CTk()
    root.geometry("800x600")
    
    # Créer le frame
    frame = ChambresFrame(root)
    frame.pack(fill="both", expand=True)
    
    # Forcer la mise à jour
    root.update()
    
    # Vérifier les enfants
    print(f"Nombre d'enfants dans le frame: {len(frame.winfo_children())}")
    
    # Lister les types de widgets
    widgets_types = {}
    for child in frame.winfo_children():
        child_type = child.__class__.__name__
        widgets_types[child_type] = widgets_types.get(child_type, 0) + 1
    
    print("Widgets trouvés:")
    for wtype, count in widgets_types.items():
        print(f"  - {wtype}: {count}")
    
    # Vérifier spécifiquement les CTkButton
    buttons = []
    def find_buttons(widget):
        if isinstance(widget, ctk.CTkButton):
            buttons.append(widget)
        for child in widget.winfo_children():
            find_buttons(child)
    
    find_buttons(frame)
    print(f"\nNombre de boutons CTkButton trouvés: {len(buttons)}")
    for btn in buttons:
        print(f"  - Bouton: '{btn.cget('text')}'")
    
    print("\nLa fenêtre va s'ouvrir. Vérifiez si les boutons sont visibles.")
    print("Fermez la fenêtre pour continuer...")
    
    root.mainloop()

if __name__ == "__main__":
    test_chambres_frame()