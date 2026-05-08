from gui.main_window import MainWindow
import customtkinter as ctk

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
    ctk.set_appearance_mode("light")  # thème clair
    ctk.set_default_color_theme("green")  # vert, bleu, etc.