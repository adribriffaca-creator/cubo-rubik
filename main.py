import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    import sys
    import os
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
    from ui.main_window import MainWindow

    app = QApplication(sys.argv)
    
    # --- ESTO ES LO QUE SOLUCIONA LA TUERCA (ICONO) EN LINUX ---
    # Debe coincidir exactamente con el nombre de tu archivo .desktop
    app.setDesktopFileName("com.github.adribriffaca_creator.cubo_rubik")
    
    # Icono por defecto (fallback) para la ventana y X11
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "cubo-rubik.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    # -----------------------------------------------------------

    window = MainWindow()
    window.show()
    sys.exit(app.exec())