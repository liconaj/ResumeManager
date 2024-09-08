import os
import json

def get_project_root() -> str:
    """Devuelve la ruta absoluta a la raíz del proyecto."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_abspath_relative_root(relative_file_path: str) -> str:
    """Retorna la ruta absoluta de un archivo relativo al archivo raiz del proyecto"""
    project_root = get_project_root()
    file_path = os.path.join(project_root, relative_file_path)
    return os.path.abspath(file_path)

def get_option(key: str) -> dict | list:
    with open(get_abspath_relative_root("data/options.json"), "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get(key, None)
