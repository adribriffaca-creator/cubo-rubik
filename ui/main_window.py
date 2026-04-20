import random
import os
import wave
import math
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QDialog, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QQuaternion, QVector3D
from PyQt6.QtMultimedia import QSoundEffect

from cube_logic import RubiksCubeLogic
from cube_renderer import CubeRenderer
from ui.panels import LeftPanel, RightPanel
from ui.celebration import CelebrationOverlay
from utils.storage import save_progress, load_progress

def generate_victory_sound():
    from pathlib import Path
    config_dir = os.path.join(Path.home(), ".config", "cubo-rubik")
    os.makedirs(config_dir, exist_ok=True)
    filename = os.path.join(config_dir, "victory.wav")
    if os.path.exists(filename): return filename
    sample_rate = 44100
    notes = [(261.63, 0.15), (329.63, 0.15), (392.00, 0.15), (523.25, 0.4)]
    with wave.open(filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for freq, duration in notes:
            num_samples = int(sample_rate * duration)
            for i in range(num_samples):
                envelope = math.sin(math.pi * i / num_samples)
                value = int(envelope * 32767.0 * math.sin(2.0 * math.pi * freq * i / sample_rate))
                f.writeframesraw(value.to_bytes(2, byteorder="little", signed=True))
    return filename

class KeyConfigDialog(QDialog):
    def __init__(self, current_mapping, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Atajos de Teclado")
        self.setFixedSize(450, 550)
        self.mapping = current_mapping
        self.inputs = {}
        
        self.setStyleSheet("""
            QDialog { background-color: #0F172A; }
            QLabel { color: #F8FAFC; font-family: 'San Francisco', Roboto; font-size: 14px; font-weight: 700; }
            QLineEdit { 
                background-color: #1E293B; color: #38BDF8; border: 2px solid #334155; 
                border-radius: 8px; padding: 8px; font-size: 18px; font-weight: 900; 
            }
            QLineEdit:focus { border: 2px solid #38BDF8; }
            QPushButton { 
                background-color: #10B981; color: white; border-radius: 12px; 
                padding: 12px; font-size: 16px; font-weight: 800; margin-top: 10px;
            }
            QPushButton:hover { background-color: #059669; }
        """)

        layout = QVBoxLayout(self)
        title = QLabel("Personalizar Controles")
        title.setStyleSheet("font-size: 20px; color: #38BDF8; font-weight: 900; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(15)
        
        order = [("U", "Arriba"), ("U'", "Arriba Inv."), ("D", "Abajo"), ("D'", "Abajo Inv."), 
                 ("R", "Derecha"), ("R'", "Derecha Inv."), ("L", "Izquierda"), ("L'", "Izquierda Inv."), 
                 ("F", "Frente"), ("F'", "Frente Inv."), ("B", "Atrás"), ("B'", "Atrás Inv.")]
        
        row, col = 0, 0
        for action, desc in order:
            lbl = QLabel(desc)
            inp = QLineEdit(self.mapping.get(action, ""))
            inp.setMaxLength(1)
            inp.setFixedWidth(50)
            inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.inputs[action] = inp
            
            h_layout = QHBoxLayout()
            h_layout.addWidget(lbl)
            h_layout.addStretch()
            h_layout.addWidget(inp)
            
            cell_widget = QWidget()
            cell_widget.setLayout(h_layout)
            cell_widget.setStyleSheet("background-color: #1E293B; border-radius: 10px; padding: 5px;")
            
            grid.addWidget(cell_widget, row, col)
            row += 1
            if row > 5:
                row = 0
                col = 1
                
        layout.addLayout(grid)
            
        btn_save = QPushButton("Guardar Cambios")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

    def get_new_mapping(self):
        return {action: inp.text().upper() for action, inp in self.inputs.items()}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador Cubo Rubik 3x3")
        
        self.key_mapping = {
            "U": "Q", "U'": "E", "L": "A", "L'": "D",
            "F": "W", "F'": "S", "D": "Z", "D'": "X",
            "R": "R", "R'": "F", "B": "B", "B'": "V"
        }
        
        self.move_queue = []
        self.queue_timer = QTimer(self)
        self.queue_timer.timeout.connect(self.process_queue)
        self.queue_timer.start(50)
        
        self.stopwatch = QTimer(self)
        self.stopwatch.timeout.connect(self.update_timer_display)
        self.time_elapsed_ms = 0
        self.is_timing = False

        snd_file = generate_victory_sound()
        self.victory_sound = QSoundEffect()
        self.victory_sound.setSource(QUrl.fromLocalFile(os.path.abspath(snd_file)))
        self.victory_sound.setVolume(0.8)
        
        self.setup_ui()
        self.apply_styles()

        # Fix para pantalla blanca: Forzar renderizado OpenGL
        self.renderer.repaint() 
        self.load_app_state()
        
        self.showMaximized()

        # Fix para Focus Stealing: Forzar a la ventana a escuchar el teclado
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

    def setup_ui(self):
        self.cube_logic = RubiksCubeLogic()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.left_panel = LeftPanel()
        self.left_panel.setFixedWidth(300)
        
        self.center_area = QWidget()
        center_layout = QVBoxLayout(self.center_area)
        center_layout.setContentsMargins(0, 0, 0, 0)
        self.renderer = CubeRenderer(self.cube_logic, self.center_area)
        center_layout.addWidget(self.renderer)

        self.right_panel = RightPanel()
        self.right_panel.setFixedWidth(300)

        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.center_area)
        main_layout.addWidget(self.right_panel)

        self.setup_connections()

    def apply_styles(self):
        self.setStyleSheet("QMainWindow { background-color: #020617; } QWidget { font-family: 'San Francisco', Roboto, sans-serif; }")
        self.left_panel.setStyleSheet("background-color: #1E293B;")
        self.right_panel.setStyleSheet("background-color: #1E293B;")
        self.center_area.setStyleSheet("background-color: #020617;")

    def setup_connections(self):
        grid = self.right_panel.layout().itemAt(1).layout()
        moves = ['U', 'D', 'R', 'L', 'F', 'B']
        for i, face in enumerate(moves):
            btn_normal = grid.itemAtPosition(i, 0).widget()
            btn_inv = grid.itemAtPosition(i, 1).widget()
            
            # Evitar que los botones roben el foco del teclado al hacerles clic
            btn_normal.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn_inv.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
            btn_normal.clicked.connect(lambda checked, f=face: self.execute_visual_move(f, False))
            btn_inv.clicked.connect(lambda checked, f=face: self.execute_visual_move(f, True))

        # Evitar robo de foco en botones de acción
        self.right_panel.btn_reset.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.right_panel.btn_scramble.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.right_panel.btn_keys.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.right_panel.btn_reset.clicked.connect(lambda: self.reset_cube(reset_camera=True))
        self.right_panel.btn_scramble.clicked.connect(self.scramble_cube)
        self.right_panel.btn_keys.clicked.connect(self.configure_keys)

    def start_timer(self):
        if not self.is_timing:
            self.is_timing = True
            self.stopwatch.start(10)

    def stop_timer(self):
        self.is_timing = False
        self.stopwatch.stop()

    def reset_timer(self):
        self.stop_timer()
        self.time_elapsed_ms = 0
        self.update_timer_display(tick=False)

    def update_timer_display(self, tick=True):
        if tick: self.time_elapsed_ms += 10
        mins = (self.time_elapsed_ms // 60000) % 60
        secs = (self.time_elapsed_ms // 1000) % 60
        cents = (self.time_elapsed_ms % 1000) // 10
        self.left_panel.timer_label.setText(f"{mins:02d}:{secs:02d}.{cents:02d}")

    def execute_visual_move(self, visual_face, inverse=False):
        logical_face = self.get_relative_face(visual_face)
        self.execute_move(logical_face, inverse)

    def execute_move(self, face, inverse=False, is_auto=False):
        if self.renderer.animating: return False
        
        if not is_auto and not self.is_timing and not self.cube_logic.is_solved():
            self.start_timer()

        def on_anim_complete():
            if not is_auto: 
                move_str = f"{face}'" if inverse else face
                self.left_panel.history_list.addItem(move_str)
                self.left_panel.history_list.scrollToBottom()
                moves_count = len(self.cube_logic.history)
                self.left_panel.moves_label.setText(f"Movimientos: {moves_count}")
                
                # Celebración si se armó manualmente
                if self.cube_logic.is_solved():
                    self.stop_timer()
                    self.victory_sound.play()
                    overlay = CelebrationOverlay(self.left_panel.timer_label.text(), moves_count, self)
                    overlay.exec()
                    # Resetea datos sin mover la cámara y devuelve el foco
                    self.reset_cube(reset_camera=False)
                    self.setFocus()

        self.renderer.animate_move(face, inverse, on_anim_complete)
        return True

    def process_queue(self):
        if self.move_queue and not self.renderer.animating:
            face, inverse, is_auto = self.move_queue.pop(0)
            self.execute_move(face, inverse, is_auto)

    def scramble_cube(self):
        self.reset_cube(reset_camera=False)
        faces = ['U', 'D', 'R', 'L', 'F', 'B']
        last_face = None
        for _ in range(20):
            face = random.choice([f for f in faces if f != last_face])
            last_face = face
            self.move_queue.append((face, random.choice([True, False]), True))

    def reset_cube(self, reset_camera=True):
        self.move_queue.clear()
        self.cube_logic.reset()
        self.reset_timer()
        self.left_panel.history_list.clear()
        self.left_panel.moves_label.setText("Movimientos: 0")
        if reset_camera:
            q_x = QQuaternion.fromAxisAndAngle(1.0, 0.0, 0.0, 25.0)
            q_y = QQuaternion.fromAxisAndAngle(0.0, 1.0, 0.0, -45.0)
            self.renderer.rotation = q_x * q_y
        self.renderer.update()

    def configure_keys(self):
        dlg = KeyConfigDialog(self.key_mapping, self)
        if dlg.exec(): 
            self.key_mapping = dlg.get_new_mapping()
        # Siempre devolver el foco a la ventana principal al cerrar el diálogo
        self.setFocus()

    def get_relative_face(self, visual_face):
        normals = {'U':(0,1,0),'D':(0,-1,0),'F':(0,0,1),'B':(0,0,-1),'R':(1,0,0),'L':(-1,0,0)}
        transformed = {}
        for face, (x, y, z) in normals.items():
            v = self.renderer.rotation.rotatedVector(QVector3D(float(x), float(y), float(z)))
            transformed[face] = (v.x(), v.y(), v.z())
        if visual_face == 'U': return max(transformed.items(), key=lambda i: i[1][1])[0]
        if visual_face == 'D': return min(transformed.items(), key=lambda i: i[1][1])[0]
        if visual_face == 'R': return max(transformed.items(), key=lambda i: i[1][0])[0]
        if visual_face == 'L': return min(transformed.items(), key=lambda i: i[1][0])[0]
        if visual_face == 'F': return max(transformed.items(), key=lambda i: i[1][2])[0]
        if visual_face == 'B': return min(transformed.items(), key=lambda i: i[1][2])[0]

    def keyPressEvent(self, event):
        key_text = event.text().upper()
        for action, mapped_key in self.key_mapping.items():
            if key_text == mapped_key:
                self.execute_visual_move(action[0], len(action) > 1)
                break

    def load_app_state(self):
        data = load_progress()
        if data:
            self.key_mapping = data.get("key_mapping", self.key_mapping)
            self.cube_logic.state = data.get("cube_state", self.cube_logic.state)
            self.cube_logic.history = data.get("history", [])
            for m in self.cube_logic.history: self.left_panel.history_list.addItem(m)
            self.left_panel.moves_label.setText(f"Movimientos: {len(self.cube_logic.history)}")
            self.time_elapsed_ms = data.get("time_elapsed_ms", 0)
            
            rot_data = data.get("camera_rotation")
            if rot_data:
                self.renderer.rotation = QQuaternion(rot_data["scalar"], rot_data["x"], rot_data["y"], rot_data["z"])
                
            self.update_timer_display(tick=False)
            self.renderer.update()

    def closeEvent(self, event):
        if self.is_timing: self.stop_timer()
        rot = self.renderer.rotation
        rot_data = {"scalar": rot.scalar(), "x": rot.x(), "y": rot.y(), "z": rot.z()}
        save_progress({"cube_state": self.cube_logic.state, "history": self.cube_logic.history, 
                       "time_elapsed_ms": self.time_elapsed_ms, "key_mapping": self.key_mapping,
                       "camera_rotation": rot_data})
        event.accept()