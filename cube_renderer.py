from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QQuaternion, QVector3D
from OpenGL.GL import *
from OpenGL.GLU import *
from cube_logic import RubiksCubeLogic
import math

class CubeRenderer(QOpenGLWidget):
    def __init__(self, logic_instance, parent=None):
        super().__init__(parent)
        self.logic = logic_instance
        
        q_x = QQuaternion.fromAxisAndAngle(1.0, 0.0, 0.0, 25.0)
        q_y = QQuaternion.fromAxisAndAngle(0.0, 1.0, 0.0, -45.0)
        self.rotation = q_x * q_y
        
        self.last_mouse_pos = None

        # Colores RGB mejorados, más brillantes y "reales"
        self.colors_rgb = {
            'U': (0.95, 0.95, 0.95), 'D': (0.98, 0.85, 0.0),
            'F': (0.9, 0.1, 0.1),    'B': (1.0, 0.45, 0.0),
            'R': (0.0, 0.2, 0.8),    'L': (0.0, 0.7, 0.2),
            'BLACK': (0.1, 0.1, 0.1)
        }

        self.animating = False
        self.anim_face = None
        self.anim_progress = 0.0
        self.anim_inverse = False
        self.on_complete_callback = None
        self.anim_speed = 0.06  # Suavidad de la animación (más bajo = más suave)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timer)
        self.timer.start(16)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glClearColor(0.05, 0.05, 0.1, 1.0)
        
        # Configurar iluminación moderna
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        
        # Posición y tipo de luz
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 10.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
        
        # Materiales (brillo)
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 30.0)
        glEnable(GL_NORMALIZE)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / float(h if h > 0 else 1), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def _on_timer(self):
        # 1. Corrección suave de Roll (Snap automático)
        max_y = -2.0
        best_axis = None
        for x, y, z in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            v = self.rotation.rotatedVector(QVector3D(float(x), float(y), float(z)))
            if v.y() > max_y:
                max_y = v.y()
                best_axis = v
                
        if best_axis:
            angle = math.degrees(math.atan2(best_axis.x(), best_axis.y()))
            if abs(angle) > 0.05:
                # Interpolar suavemente hacia la alineación correcta
                correct = QQuaternion.fromAxisAndAngle(0.0, 0.0, 1.0, angle * 0.1)
                self.rotation = correct * self.rotation
                self.rotation.normalize()

        # 2. Renderizar escena
        self.update()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -11.0)
        
        axis, angle = self.rotation.getAxisAndAngle()
        glRotatef(angle, axis.x(), axis.y(), axis.z())
        
        self.draw_cube()

    def animate_move(self, face, inverse=False, on_complete=None):
        if self.animating: return
        self.animating = True
        self.anim_face = face
        self.anim_inverse = inverse
        self.anim_progress = 0.0
        self.on_complete_callback = on_complete

    def draw_cube(self):
        current_anim_angle = 0.0
        if self.animating:
            self.anim_progress += self.anim_speed
            if self.anim_progress >= 1.0:
                self.anim_progress = 1.0
                
            # Easing function (suave al inicio y al final)
            p = self.anim_progress
            ease_p = p * p * (3.0 - 2.0 * p)
            target = 90.0 if self.anim_inverse else -90.0
            current_anim_angle = ease_p * target

            if self.anim_progress >= 1.0:
                self.animating = False
                self.logic.apply_move(self.anim_face, self.anim_inverse)
                current_anim_angle = 0.0
                if self.on_complete_callback: self.on_complete_callback()

        idx_func = RubiksCubeLogic.get_sticker_index
        state = self.logic.state

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if x == 0 and y == 0 and z == 0: continue
                    
                    glPushMatrix()
                    
                    # 1. Animación de cara
                    is_moving = False
                    if self.animating or current_anim_angle != 0.0:
                        f = self.anim_face
                        if f == 'U' and y == 1: is_moving = True
                        elif f == 'D' and y == -1: is_moving = True
                        elif f == 'L' and x == -1: is_moving = True
                        elif f == 'R' and x == 1: is_moving = True
                        elif f == 'F' and z == 1: is_moving = True
                        elif f == 'B' and z == -1: is_moving = True
                    
                    if is_moving:
                        f = self.anim_face
                        if f == 'U': glRotatef(current_anim_angle, 0, 1, 0)
                        elif f == 'D': glRotatef(-current_anim_angle, 0, 1, 0)
                        elif f == 'L': glRotatef(-current_anim_angle, 1, 0, 0)
                        elif f == 'R': glRotatef(current_anim_angle, 1, 0, 0)
                        elif f == 'F': glRotatef(current_anim_angle, 0, 0, 1)
                        elif f == 'B': glRotatef(-current_anim_angle, 0, 0, 1)

                    # 2. Separación entre piezas (efecto de cubo real)
                    glTranslatef(x * 1.05, y * 1.05, z * 1.05)
                    
                    self.draw_cubie_with_stickers(x, y, z, state, idx_func)
                    glPopMatrix()

    def draw_cubie_with_stickers(self, x, y, z, state, idx_func):
        r = 0.47 # Pieza plástica negra
        d = 0.48 # Altura del sticker (muy ligeramente sobresaliente)
        s = 0.43 # Tamaño del sticker (deja un borde negro)
        
        # Cuerpo del cubie
        glColor3fv(self.colors_rgb['BLACK'])
        self._draw_box(r)

        # TOP
        if y == 1:
            c = state['U'][idx_func('U', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            glNormal3f(0, 1, 0)
            self._draw_quad(((s,d,s), (s,d,-s), (-s,d,-s), (-s,d,s)))
        # BOTTOM
        if y == -1:
            c = state['D'][idx_func('D', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            glNormal3f(0, -1, 0)
            self._draw_quad(((s,-d,-s), (s,-d,s), (-s,-d,s), (-s,-d,-s)))
        # FRONT
        if z == 1:
            c = state['F'][idx_func('F', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            glNormal3f(0, 0, 1)
            self._draw_quad(((s,s,d), (-s,s,d), (-s,-s,d), (s,-s,d)))
        # BACK
        if z == -1:
            c = state['B'][idx_func('B', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            glNormal3f(0, 0, -1)
            self._draw_quad(((-s,s,-d), (s,s,-d), (s,-s,-d), (-s,-s,-d)))
        # RIGHT
        if x == 1:
            c = state['R'][idx_func('R', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            glNormal3f(1, 0, 0)
            self._draw_quad(((d,s,-s), (d,s,s), (d,-s,s), (d,-s,-s)))
        # LEFT
        if x == -1:
            c = state['L'][idx_func('L', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            glNormal3f(-1, 0, 0)
            self._draw_quad(((-d,s,s), (-d,s,-s), (-d,-s,-s), (-d,-s,s)))

    def _draw_box(self, r):
        glBegin(GL_QUADS)
        # Y+
        glNormal3f(0, 1, 0)
        glVertex3f(r,r,r); glVertex3f(r,r,-r); glVertex3f(-r,r,-r); glVertex3f(-r,r,r)
        # Y-
        glNormal3f(0, -1, 0)
        glVertex3f(r,-r,-r); glVertex3f(r,-r,r); glVertex3f(-r,-r,r); glVertex3f(-r,-r,-r)
        # Z+
        glNormal3f(0, 0, 1)
        glVertex3f(r,r,r); glVertex3f(-r,r,r); glVertex3f(-r,-r,r); glVertex3f(r,-r,r)
        # Z-
        glNormal3f(0, 0, -1)
        glVertex3f(-r,r,-r); glVertex3f(r,r,-r); glVertex3f(r,-r,-r); glVertex3f(-r,-r,-r)
        # X+
        glNormal3f(1, 0, 0)
        glVertex3f(r,r,-r); glVertex3f(r,r,r); glVertex3f(r,-r,r); glVertex3f(r,-r,-r)
        # X-
        glNormal3f(-1, 0, 0)
        glVertex3f(-r,r,r); glVertex3f(-r,r,-r); glVertex3f(-r,-r,-r); glVertex3f(-r,-r,r)
        glEnd()

    def _draw_quad(self, v):
        glBegin(GL_QUADS)
        for i in range(4): glVertex3f(*v[i])
        glEnd()

    def mousePressEvent(self, e): self.last_mouse_pos = e.position()
    def mouseMoveEvent(self, e):
        if self.last_mouse_pos:
            p = e.position()
            dx = p.x() - self.last_mouse_pos.x()
            dy = p.y() - self.last_mouse_pos.y()
            
            rot_y = QQuaternion.fromAxisAndAngle(0.0, 1.0, 0.0, dx * 0.5)
            rot_x = QQuaternion.fromAxisAndAngle(1.0, 0.0, 0.0, dy * 0.5)
            
            self.rotation = rot_x * rot_y * self.rotation
            self.rotation.normalize()
            
            self.last_mouse_pos = p
