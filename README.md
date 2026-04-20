# 🧊 Simulador Interactivo de Cubo Rubik 3x3

Un simulador de Cubo Rubik premium desarrollado en **Python** utilizando **PyQt6** y **OpenGL**. Esta aplicación ofrece una experiencia fluida con gráficos 3D realistas, iluminación de materiales, físicas de separación y una rotación libre de 360°, diseñada para entusiastas del speedcubing y programadores.

![Captura del Simulador](assets/cubo-rubik.png)

---

## ✨ Características Principales

* **Motor 3D de Alto Rendimiento:** Renderizado basado en OpenGL con libertad de movimiento absoluta sin bloqueos de cardán (Gimbal Lock) usando Cuaterniones.
* **Auto-Nivelación (Snap Roll):** La cámara corrige automáticamente la inclinación para mantener el cubo derecho durante las rotaciones libres.
* **Gráficos Realistas:** Iluminación ambiental y difusa, con materiales que simulan plástico real y separación física entre las piezas.
* **Animaciones Suaves:** Curvas de aceleración (*easing*) en cada rotación, con colores anclados matemáticamente a la lógica del juego.
* **Gestión de Estado Persistente:** Guarda automáticamente tu progreso, tiempo e incluso el ángulo de la cámara exacto al cerrar la aplicación.
* **Interfaz Adaptativa:** Historial de movimientos, mezclador automático y controles en pantalla.
* **Personalización:** Sistema de remapeo de teclas integrado.

---

## 🎮 Guía de Controles

### Interacción con el Ratón
* **Órbita Libre:** Haz **clic izquierdo y arrastra** en cualquier dirección para rotar el cubo libremente. El sistema de auto-nivelación mantendrá el cubo derecho al soltar el clic.

### Controles de Teclado
Puedes configurar tus propias teclas en la aplicación. Los controles por defecto (Notación Singmaster) son:
| Cara | Giro Horario | Giro Antihorario |
| :--- | :---: | :---: |
| **Superior (U)** | `Q` | `E` |
| **Frontal (F)** | `W` | `S` |
| **Izquierda (L)** | `A` | `D` |
| **Derecha (R)** | `R` | `F` |
| **Inferior (D)** | `Z` | `X` |
| **Trasera (B)** | `B` | `V` |

---

## 🚀 Guía de Instalación Detallada

### 🐧 Arch Linux, CachyOS, Manjaro, EndeavourOS
El simulador está publicado de forma oficial en el **Arch User Repository (AUR)**. Puedes instalarlo como cualquier otra aplicación nativa del sistema, lo que te creará un acceso directo en tu menú de aplicaciones.

Usando **yay**:
```bash
yay -S cubo-rubik-git
```

Usando **paru**:
```bash
paru -S cubo-rubik-git
```

Una vez instalado, simplemente busca "Simulador Cubo Rubik" en tu lanzador de aplicaciones o ejecuta `cubo-rubik` en tu terminal.

---

### 🪟 Windows
1. Descarga el código fuente haciendo clic en **Code -> Download ZIP** o ve a la sección **Releases** si hay ejecutables disponibles.
2. Si descargaste el ZIP, extráelo en una carpeta.
3. Asegúrate de tener **Python** instalado en tu sistema (puedes descargarlo desde python.org, asegúrate de marcar la casilla "Add Python to PATH" durante la instalación).
4. Abre la consola (CMD o PowerShell) en la carpeta donde extrajiste el juego.
5. Instala las librerías necesarias ejecutando:
   ```cmd
   pip install PyQt6 PyOpenGL
   ```
6. Ejecuta el juego con:
   ```cmd
   python main.py
   ```

---

### 🐧 Ubuntu, Debian, Linux Mint, Fedora (Clonación manual)

Para el resto de distribuciones de Linux, lo ideal es instalar las dependencias base de tu sistema y luego clonar el código.

#### 1. Instalar dependencias

**Ubuntu / Debian / Linux Mint / Pop!_OS:**
```bash
sudo apt update
sudo apt install python3-pyqt6 python3-opengl git
```

**Fedora / Nobara / Red Hat:**
```bash
sudo dnf install python3-pyqt6 python3-opengl git
```

#### 2. Clonar y Ejecutar
Abre una terminal y descarga el código fuente:
```bash
git clone https://github.com/adribriffaca-creator/cubo-rubik.git
cd cubo-rubik
```

Lanza el programa:
```bash
python3 main.py
```

---

### 🍏 macOS
Clona el proyecto:
```bash
git clone https://github.com/adribriffaca-creator/cubo-rubik.git
cd cubo-rubik
```

Instala las librerías usando pip:
```bash
pip3 install PyQt6 PyOpenGL
```

Ejecuta el juego:
```bash
python3 main.py
```

---

## 🛠️ Solución de Problemas
* **La ventana se cierra sola o muestra gráficos corruptos:** Asegúrate de tener los drivers de video (Nvidia/AMD/Intel) actualizados. OpenGL requiere soporte de aceleración por hardware.
* **Wayland (Linux):** Si experimentas parpadeos de la ventana en Wayland (Gnome/KDE), puedes forzar el modo X11 lanzando la app con `QT_QPA_PLATFORM=xcb cubo-rubik` o `QT_QPA_PLATFORM=xcb python3 main.py`.