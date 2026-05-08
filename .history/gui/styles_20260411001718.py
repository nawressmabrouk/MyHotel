import customtkinter as ctk
from tkinter import ttk

def configure_treeview_styles():
    """Configure les styles pour tous les Treeview"""
    style = ttk.Style()
    
    # Base theme
    style.theme_use("clam")
    
    # Configuration selon le thème CustomTkinter
    if ctk.get_appearance_mode() == "Light":
        # Style pour l'en-tête
        style.configure("Custom.Treeview.Heading",
            background="#e67e22",
            foreground="white",
            font=("Arial", 13, "bold"),
            relief="flat",
            borderwidth=0,
            padding=(10, 8)
        )
        style.map("Custom.Treeview.Heading",
            background=[('active', '#d35400')]
        )
        
        # Style pour les lignes
        style.configure("Custom.Treeview",
            background="white",
            foreground="#2c3e50",
            rowheight=40,
            fieldbackground="white",
            font=("Arial", 11),
            borderwidth=0,
            highlightthickness=0
        )
        
        style.map("Custom.Treeview",
            background=[('selected', '#3a7eb6')],
            foreground=[('selected', 'white')]
        )
        
    else:  # Dark mode
        style.configure("Custom.Treeview.Heading",
            background="#e67e22",
            foreground="white",
            font=("Arial", 13, "bold"),
            relief="flat",
            borderwidth=0,
            padding=(10, 8)
        )
        style.map("Custom.Treeview.Heading",
            background=[('active', '#d35400')]
        )
        
        style.configure("Custom.Treeview",
            background="#2b2b2b",
            foreground="#ecf0f1",
            rowheight=40,
            fieldbackground="#2b2b2b",
            font=("Arial", 11),
            borderwidth=0,
            highlightthickness=0
        )
        
        style.map("Custom.Treeview",
            background=[('selected', '#3a7eb6')],
            foreground=[('selected', 'white')]
        )
    
    # Style pour les scrollbars
    style.configure("Custom.Vertical.TScrollbar",
        background="#e67e22",
        troughcolor="#f0f0f0",
        arrowcolor="white",
        bordercolor="#e67e22",
        lightcolor="#e67e22",
        darkcolor="#d35400",
        width=12
    )
    
    style.map("Custom.Vertical.TScrollbar",
        background=[('active', '#d35400')]
    )
    
    return style


def apply_alternate_colors(treeview):
    """Applique des couleurs alternées aux lignes du Treeview"""
    items = treeview.get_children()
    for i, item in enumerate(items):
        if ctk.get_appearance_mode() == "Light":
            if i % 2 == 0:
                treeview.tag_configure('even', background='#f8f9fa')
                treeview.item(item, tags=('even',))
            else:
                treeview.tag_configure('odd', background='#ffffff')
                treeview.item(item, tags=('odd',))
        else:
            if i % 2 == 0:
                treeview.tag_configure('even', background='#333333')
                treeview.item(item, tags=('even',))
            else:
                treeview.tag_configure('odd', background='#2b2b2b')
                treeview.item(item, tags=('odd',))