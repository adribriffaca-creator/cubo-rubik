from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
from cube_logic import RubiksCubeLogic

class CubeRenderer(QOpenGLWidget):
    def __init__(self, logic_instance, parent=None):
        super().__init__(parent)
        self.logic = logic_instance
        self.rot_x, self.rot_y = 25.0, -45.0
        self.last_mouse_pos = None

        # Colores RGB estándar
        self.colors_rgb = {
            'U': (1.0, 1.0, 1.0), 'D': (1.0, 0.93, 0.0),
            'F': (1.0, 0.15, 0.0), 'B': (1.0, 0.50, 0.0),
            'R': (0.0, 0.27, 0.67), 'L': (0.0, 0.60, 0.28),
            'BLACK': (0.07, 0.07, 0.07)
        }

        self.animating = False
        self.anim_face = None
        self.anim_angle = 0.0
        self.anim_target = 0.0
        self.anim_step = 0.0
        self.anim_inverse = False
        self.on_complete_callback = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glClearColor(0.1, 0.1, 0.18, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / float(h if h > 0 else 1), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -11.0)
        glRotatef(self.rot_x, 1.0, 0.0, 0.0)
        glRotatef(self.rot_y, 0.0, 1.0, 0.0)
        self.draw_cube()

    def animate_move(self, face, inverse=False, on_complete=None):
        if self.animating: return
        self.animating = True
        self.anim_face = face
        self.anim_inverse = inverse
        self.anim_angle = 0.0
        self.anim_target = 90.0 if inverse else -90.0
        self.anim_step = self.anim_target / 10.0 # Más rápido para fluidez
        self.on_complete_callback = on_complete

    def draw_cube(self):
        if self.animating:
            self.anim_angle += self.anim_step
            if abs(self.anim_angle) >= abs(self.anim_target):
                self.anim_angle = self.anim_target
                self.animating = False
                # Aquí es donde la lógica se pone al día con la realidad visual
                self.logic.apply_move(self.anim_face, self.anim_inverse)
                if self.on_complete_callback: self.on_complete_callback()

        idx_func = RubiksCubeLogic.get_sticker_index
        state = self.logic.state

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if x == 0 and y == 0 and z == 0: continue
                    
                    glPushMatrix()
                    
                    # 1. Determinamos si esta pieza pertenece a la cara que está girando
                    is_moving = False
                    if self.animating:
                        f = self.anim_face
                        if f == 'U' and y == 1: is_moving = True
                        elif f == 'D' and y == -1: is_moving = True
                        elif f == 'L' and x == -1: is_moving = True
                        elif f == 'R' and x == 1: is_moving = True
                        elif f == 'F' and z == 1: is_moving = True
                        elif f == 'B' and z == -1: is_moving = True
                    
                    # 2. Si se mueve, aplicamos la rotación física
                    if is_moving:
                        f = self.anim_face
                        if f == 'U': glRotatef(self.anim_angle, 0, 1, 0)
                        elif f == 'D': glRotatef(-self.anim_angle, 0, 1, 0)
                        elif f == 'L': glRotatef(-self.anim_angle, 1, 0, 0)
                        elif f == 'R': glRotatef(self.anim_angle, 1, 0, 0)
                        elif f == 'F': glRotatef(self.anim_angle, 0, 0, 1)
                        elif f == 'B': glRotatef(-self.anim_angle, 0, 0, 1)

                    # 3. Posicionamos el cubie
                    glTranslatef(x * 1.05, y * 1.05, z * 1.05)
                    
                    # 4. Dibujamos los stickers
                    # IMPORTANTE: Pasamos x, y, z originales para que el color no cambie MIENTRAS se mueve
                    self.draw_cubie_with_stickers(x, y, z, state, idx_func)
                    glPopMatrix()

    def draw_cubie_with_stickers(self, x, y, z, state, idx_func):
        r, d = 0.48, 0.492 # Stickers ligeramente más afuera para evitar z-fighting
        
        # Cuerpo del cubie
        glColor3fv(self.colors_rgb['BLACK'])
        self._draw_box(r)

        # Solo dibujamos los stickers que dan al exterior
        # TOP
        if y == 1:
            c = state['U'][idx_func('U', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            self._draw_quad(((r,d,r), (r,d,-r), (-r,d,-r), (-r,d,r)))
        # BOTTOM
        if y == -1:
            c = state['D'][idx_func('D', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            self._draw_quad(((r,-d,-r), (r,-d,r), (-r,-d,r), (-r,-d,-r)))
        # FRONT
        if z == 1:
            c = state['F'][idx_func('F', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            self._draw_quad(((r,r,d), (-r,r,d), (-r,-r,d), (r,-r,d)))
        # BACK
        if z == -1:
            c = state['B'][idx_func('B', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            self._draw_quad(((-r,r,-d), (r,r,-d), (r,-r,-d), (-r,-r,-d)))
        # RIGHT
        if x == 1:
            c = state['R'][idx_func('R', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            self._draw_quad(((d,r,-r), (d,r,r), (d,-r,r), (d,-r,-r)))
        # LEFT
        if x == -1:
            c = state['L'][idx_func('L', x, y, z)]
            glColor3fv(self.colors_rgb[c])
            self._draw_quad(((-d,r,r), (-d,r,-r), (-d,-r,-r), (-d,-r,r)))

    def _draw_box(self, r):
        glBegin(GL_QUADS)
        # Dibujar las 6 caras del cubo interno
        glVertex3f(r,r,r); glVertex3f(r,r,-r); glVertex3f(-r,r,-r); glVertex3f(-r,r,r)
        glVertex3f(r,-r,-r); glVertex3f(r,-r,r); glVertex3f(-r,-r,r); glVertex3f(-r,-r,-r)
        glVertex3f(r,r,r); glVertex3f(-r,r,r); glVertex3f(-r,-r,r); glVertex3f(r,-r,r)
        glVertex3f(-r,r,-r); glVertex3f(r,r,-r); glVertex3f(r,-r,-r); glVertex3f(-r,-r,-r)
        glVertex3f(r,r,-r); glVertex3f(r,r,r); glVertex3f(r,-r,r); glVertex3f(r,-r,-r)
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
            self.rot_y += (p.x() - self.last_mouse_pos.x()) * 0.5
            self.rot_x += (p.y() - self.last_mouse_pos.y()) * 0.5
            self.last_mouse_pos = p