import json
import os
from pathlib import Path

# Obtener el directorio de configuración del usuario
CONFIG_DIR = os.path.join(Path.home(), ".config", "cubo-rubik")
SAVE_FILE = os.path.join(CONFIG_DIR, "save_data.json")

def ensure_config_dir():
    """Asegura que el directorio de configuración exista."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

def save_progress(data):
    """Guarda el estado del cubo y la app en un archivo JSON."""
    ensure_config_dir()
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error al guardar progreso: {e}")

def load_progress():
    """Carga el estado de la app desde el archivo JSON si existe."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar progreso: {e}")
    return None