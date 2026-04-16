import json
import os

SAVE_FILE = "save_data.json"

def save_progress(data):
    """Guarda el estado del cubo y la app en un archivo JSON."""
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