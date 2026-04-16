# 🧊 Simulador Interactivo de Cubo Rubik 3x3

Un simulador de Cubo Rubik premium desarrollado en **Python** utilizando **PyQt6** y **OpenGL**. Esta aplicación ofrece una experiencia fluida con gráficos 3D realistas, diseñada específicamente para entusiastas del speedcubing y programadores interesados en gráficos por computadora.

![Captura del Simulador](assets/cubo-rubik.png)

## ✨ Características Principales

* **Motor 3D de Alto Rendimiento:** Renderizado basado en OpenGL con iluminación dinámica y sombreado de caras.
* **Cronómetro de Precisión:** Medición automática que se activa al primer movimiento, con precisión de milisegundos.
* **Gestión de Estado:** El cubo guarda automáticamente su posición y el tiempo transcurrido al cerrar la aplicación.
* **Interfaz Adaptativa:** Paneles laterales con historial de movimientos y controles manuales.
* **Personalización Total:** Sistema de remapeo de teclas para adaptar los giros a tu comodidad.
* **Efectos de Sonido:** Feedback auditivo y celebración al resolver el cubo.

## 🎮 Guía de Controles

El simulador permite el control tanto por mouse como por teclado.

### Movimientos del Teclado (Sistema Singmaster)
| Cara | Giro Horario | Giro Antihorario |
| :--- | :---: | :---: |
| **Superior (Up)** | `Q` | `E` |
| **Frontal (Front)** | `W` | `S` |
| **Izquierda (Left)** | `A` | `D` |
| **Derecha (Right)** | `R` | `F` |
| **Inferior (Down)** | `Z` | `X` |
| **Trasera (Back)** | `B` | `V` |

### Interacción con Mouse
* **Rotación de Cámara:** Haz clic izquierdo y arrastra en el área del cubo para observar cualquier ángulo.
* **Controles Manuales:** Usa los botones del panel derecho para ejecutar movimientos precisos con el cursor.

## 🚀 Instalación y Ejecución

### Requisitos Previos
Necesitas tener instalado Python 3.10+ y los controladores de video actualizados para soporte OpenGL.

### En Fedora Linux
```bash
# Instalar dependencias del sistema
sudo dnf install python3-pyqt6 python3-opengl

# Clonar el repositorio
git clone [https://github.com/adribriffaca-creator/cubo-rubik.git](https://github.com/adribriffaca-creator/cubo-rubik.git)
cd cubo-rubik

# Ejecutar la aplicación
python3 main.py
