import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow

def resource_path(relative_path):
    """ Obtiene la ruta absoluta para el recurso, funciona para dev y para PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    
    # --- ESTO ES LO QUE SOLUCIONA LA TUERCA (ICONO) EN LINUX ---
    # Debe coincidir exactamente con el nombre de tu archivo .desktop
    app.setDesktopFileName("cubo-rubik")
    
    # Icono por defecto (fallback) para la ventana y X11
    icon_path = resource_path(os.path.join("assets", "cubo-rubik.png"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    # -----------------------------------------------------------

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()