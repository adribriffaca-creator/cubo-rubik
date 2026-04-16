from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QGridLayout
from PyQt6.QtCore import Qt

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 25, 20, 25)
        
        title_style = """
            background-color: #0F172A;
            color: #7DD3FC;
            border-radius: 8px;
            padding: 8px;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.5px;
        """
        
        lbl_tiempo = QLabel("CRONÓMETRO")
        lbl_tiempo.setStyleSheet(title_style)
        lbl_tiempo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer_label = QLabel("00:00.00")
        self.timer_label.setStyleSheet("""
            background-color: #0F172A; 
            color: #38BDF8; 
            border-radius: 12px; 
            padding: 15px; 
            font-size: 44px; 
            font-weight: 900;
            font-family: 'Consolas', 'Courier New', monospace;
            border: 2px solid #334155;
        """)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.moves_label = QLabel("Movimientos: 0")
        self.moves_label.setStyleSheet("""
            background-color: #0F172A;
            color: #94A3B8;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
            font-weight: 700;
            margin-top: 5px;
        """)
        self.moves_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        lbl_historial = QLabel("HISTORIAL DE MOVIMIENTOS")
        lbl_historial.setStyleSheet(title_style)
        lbl_historial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget { 
                background-color: #0F172A; 
                border-radius: 12px; 
                padding: 12px; 
                font-size: 16px; 
                font-weight: bold; 
                color: #F8FAFC;
                border: 2px solid #334155;
            }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #1E293B; }
            QListWidget::item:selected { background-color: #38BDF8; color: #0F172A; border-radius: 6px; }
        """)

        layout.addWidget(lbl_tiempo)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.moves_label)
        layout.addSpacing(25)
        layout.addWidget(lbl_historial)
        layout.addWidget(self.history_list)

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 25, 20, 25)
        
        title = QLabel("CONTROLES MANUALES")
        title.setStyleSheet("""
            background-color: #0F172A;
            color: #7DD3FC;
            border-radius: 8px;
            padding: 8px;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.5px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        grid = QGridLayout()
        grid.setSpacing(12)
        moves = ['U', 'D', 'R', 'L', 'F', 'B']
        
        btn_style = """
            QPushButton { 
                background-color: #334155; 
                border-radius: 10px; 
                padding: 14px; 
                font-weight: 900; 
                font-size: 18px; 
                color: #F8FAFC; 
                border: 1px solid #475569;
            }
            QPushButton:hover { 
                background-color: #475569; 
                color: #38BDF8; 
                border-color: #38BDF8; 
            }
            QPushButton:pressed { background-color: #1E293B; }
        """
        
        for i, move in enumerate(moves):
            btn = QPushButton(move)
            btn_inv = QPushButton(f"{move}'")
            btn.setStyleSheet(btn_style)
            btn_inv.setStyleSheet(btn_style)
            grid.addWidget(btn, i, 0)
            grid.addWidget(btn_inv, i, 1)
            
        layout.addLayout(grid)
        layout.addStretch()
        
        self.btn_scramble = QPushButton("Mezclar")
        self.btn_scramble.setStyleSheet(self._action_style("#1E3A8A", "#1D4ED8"))
        
        self.btn_reset = QPushButton("Reiniciar")
        self.btn_reset.setStyleSheet(self._action_style("#881337", "#BE123C"))
        
        self.btn_keys = QPushButton("Configurar Teclas")
        self.btn_keys.setStyleSheet(self._action_style("#134E4A", "#0F766E"))
        
        # Lista actualizada sin btn_solve
        for btn in [self.btn_scramble, self.btn_reset, self.btn_keys]:
            layout.addWidget(btn)

    def _action_style(self, base_color, hover_color):
        return f"""
            QPushButton {{
                background-color: {base_color}; 
                color: #F8FAFC; 
                border-radius: 10px;
                padding: 14px; 
                font-size: 15px; 
                font-weight: 800; 
                border: 1px solid #0F172A; 
                margin-top: 5px;
            }}
            QPushButton:hover {{ 
                background-color: {hover_color}; 
                border-color: {hover_color}; 
            }}
            QPushButton:pressed {{ 
                opacity: 0.7; 
            }}
        """