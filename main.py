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
    from PyQt6.QtWidgets import QApplication
    from ui.main_window import MainWindow

    app = QApplication(sys.argv)
    
    # --- ESTO ES LO QUE SOLUCIONA LA TUERCA ---
    # Debe coincidir exactamente con el nombre de tu archivo .desktop (sin el .desktop)
    # En main.py
    app.setDesktopFileName("com.github.adribriffaca_creator.cubo_rubik")
    # ------------------------------------------

    window = MainWindow()
    window.show()
    sys.exit(app.exec())