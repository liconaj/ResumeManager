import os
import json
import re
import unicodedata
from difflib import get_close_matches, SequenceMatcher
from datetime import datetime
import webbrowser

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

def normalize_string(text):
    """Elimina caracteres especiales y convierte el texto a minúsculas."""
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9\s]', '', text.lower()).strip()

def get_closest_match(items: list[str], target: str, default_value = "") -> str:
    matches = get_close_matches(target, items, n=2)
    return matches[0] if matches else default_value

def match(a: str, b: str, threshold: float = 0.9) -> bool:
    return SequenceMatcher(None, normalize_string(a), normalize_string(b)).ratio() >= threshold

def open_link(link: str) -> None:
    if link:
        webbrowser.open(link)

def gen_list_of_years(start: int, end: int = datetime.now().year):
    return [str(year) for year in range(end, start-1, -1)]

def calc_age(birthdate_str: str) -> str:
    if not birthdate_str:
        return ""
    try:
        birthdate = datetime.strptime(birthdate_str, "%d/%m/%Y")
    except Exception:
        birthdate = datetime.strptime("1/11/1111", "%d/%m/%Y")
    today = datetime.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return str(age)
