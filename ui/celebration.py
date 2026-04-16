from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class CelebrationOverlay(QDialog):
    def __init__(self, time_str, moves, parent=None):
        super().__init__(parent)
        # Hace que la ventana no tenga bordes del sistema operativo y sea flotante
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Contenedor principal con efecto cristal oscuro (Glassmorphism)
        container = QLabel()
        container.setStyleSheet("""
            background-color: rgba(28, 28, 30, 0.95);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("🎉 ¡Cubo Resuelto! 🎉")
        title.setStyleSheet("color: #34c759; font-size: 28px; font-weight: 900; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        stats = QLabel(f"Tiempo: {time_str}\nMovimientos: {moves}")
        stats.setStyleSheet("color: white; font-size: 20px; font-weight: 600; line-height: 1.5;")
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_close = QPushButton("Genial")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #0a84ff; color: white; border-radius: 12px;
                padding: 10px 30px; font-size: 16px; font-weight: bold; margin-top: 20px;
            }
            QPushButton:hover { background-color: #007aff; }
        """)
        btn_close.clicked.connect(self.accept)

        container_layout.addWidget(title)
        container_layout.addWidget(stats)
        container_layout.addWidget(btn_close)

        layout.addWidget(container)