# 🧊 Simulador Interactivo de Cubo Rubik 3x3

Un simulador de Cubo Rubik premium desarrollado en **Python** utilizando **PyQt6** y **OpenGL**. Esta aplicación ofrece una experiencia fluida con gráficos 3D realistas y rotación libre de 360°, diseñada para entusiastas del speedcubing y programadores.

![Captura del Simulador](assets/cubo-rubik.png)

---

## ✨ Características Principales

* **Motor 3D de Alto Rendimiento:** Renderizado basado en OpenGL con libertad de movimiento absoluta (sin bloqueos de cámara).
* **Cronómetro de Precisión:** Medición automática que se activa al primer movimiento.
* **Gestión de Estado Persistente:** Guarda automáticamente tu progreso y tiempo al cerrar.
* **Interfaz Adaptativa:** Historial de movimientos y botones de rotación de cámara.
* **Personalización:** Sistema de remapeo de teclas integrado.
* **Efectos de Sonido:** Feedback auditivo al girar y celebración al resolver.

---

## 🎮 Guía de Controles

### Movimientos del Teclado (Notación Singmaster)
| Cara | Giro Horario | Giro Antihorario |
| :--- | :---: | :---: |
| **Superior (Up)** | `Q` | `E` |
| **Frontal (Front)** | `W` | `S` |
| **Izquierda (Left)** | `A` | `D` |
| **Derecha (Right)** | `R` | `F` |
| **Inferior (Down)** | `Z` | `X` |
| **Trasera (Back)** | `B` | `V` |

### Interacción con Mouse
* **Órbita Libre:** Haz **clic izquierdo y arrastra** para rotar el cubo desde cualquier ángulo. Esto te permite moverte por los laterales de cualquier cara (incluyendo la roja, verde, etc.) sin restricciones.
* **Botones Laterales:** Usa las flechas (◀, ▶, ▲, ▼) en el panel derecho para girar el cubo en pasos de 90°.

---

## 🚀 Guía de Instalación Detallada

### 🪟 Instalación en Windows
Si no quieres usar la terminal, este es el método para ti:
1. Ve a la sección **[Releases]** en el panel lateral derecho de este repositorio.
2. Descarga el archivo `.exe` o el `.zip` de la última versión.
3. Si es un zip, extráelo. Haz doble clic en `CuboRubik.exe` y ¡a jugar!

---

### 🐧 Instalación en Linux (Paso a Paso)

Para Linux, lo ideal es instalar las dependencias de tu sistema y luego clonar el código.

#### 1. Instalar dependencias según tu distribución:

* **Ubuntu / Debian / Linux Mint / Pop!_OS:**
  ```bash
  sudo apt update
  sudo apt install python3-pyqt6 python3-opengl git
Fedora / Nobara / Red Hat:

Bash
sudo dnf install python3-pyqt6 python3-opengl git
Arch Linux / Manjaro / EndeavourOS:

Bash
sudo pacman -S python-pyqt6 python-opengl git
2. Clonar el repositorio (Descargar el código fuente)
La clonación es el proceso de descargar una copia idéntica de este proyecto desde GitHub a tu ordenador. Esto crea una carpeta con todos los archivos necesarios y mantiene una conexión con este repositorio para futuras actualizaciones.
Para hacerlo, abre una terminal y escribe:

Bash
git clone [https://github.com/adribriffaca-creator/cubo-rubik.git](https://github.com/adribriffaca-creator/cubo-rubik.git)
3. Ejecutar la aplicación
Una vez descargado, entra en la carpeta y lanza el programa:

Bash
cd cubo-rubik
python3 main.py
🍏 Instalación en macOS o mediante PIP
Si prefieres usar el gestor de paquetes de Python de forma universal:

Clona el proyecto:

Bash
git clone [https://github.com/adribriffaca-creator/cubo-rubik.git](https://github.com/adribriffaca-creator/cubo-rubik.git)
cd cubo-rubik
Instala las librerías necesarias:

Bash
pip install PyQt6 PyOpenGL
Ejecuta:

Bash
python main.py
🛠️ Solución de Problemas
La ventana se cierra sola: Asegúrate de tener tus drivers de video actualizados. OpenGL requiere soporte de hardware para funcionar.
Error de Importación: Si el sistema indica que falta PyQt6, asegúrate de haber ejecutado el comando de instalación de tu distribución o el comando pip install.
