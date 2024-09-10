import os
import json
import re
import urllib.parse
import unicodedata
from difflib import get_close_matches, SequenceMatcher
from datetime import datetime
import webbrowser
import hashlib
import secrets
import time

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

def get_unsensitive_close_matches(word, possibilities, n=3, cutoff=0.6):
    """
    Encuentra lista de coincidiencias suficientemente buenas
    comparando valores normalizados
    """
    normalized_word = normalize_string(word)
    normalized_possibilities = [normalize_string(str(s)) for s in possibilities]
    close_normalized_matches = get_close_matches(normalized_word, normalized_possibilities, n, cutoff)
    close_matches = []
    for cnm in close_normalized_matches:
        index = normalized_possibilities.index(cnm)
        close_matches.append(possibilities[index])
    return close_matches

def get_closest_match(possibilities: list[str], word: str, default_value = "") -> str:
    matches = get_unsensitive_close_matches(word, possibilities, n=2)
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

def format_identity_document_type(id_doc_type: str) -> str:
    id_doc_types_list = get_option("id_document_type")
    return get_closest_match(id_doc_types_list, id_doc_type)

def format_motivations(motivations: str) -> str:
    motivations_formated = []
    for m in motivations.split(","):
        m = get_closest_match(get_option("motivations"), m, None)
        if m is None:
            continue
        motivations_formated.append(m.strip())
    return ",".join(motivations_formated)

def format_place(department_name: str, city_name: str) -> tuple[str, str]:
    department_cities = get_option("department_cities")
    departments = list(department_cities.keys())
    if "bogota" in  normalize_string(city_name):
        department_name = get_closest_match(departments, "bogota dc")
    department_name_formated = get_closest_match(departments, department_name)

    cities = department_cities.get(department_name_formated, [])
    city_name_formated = get_closest_match(cities, city_name)
    return department_name_formated, city_name_formated
    
def format_gender(gender: str) -> str:
    genders = get_option("gender")
    return get_closest_match(genders, gender, "Otro")

def format_ethnicity(ethnicity: str) -> str:
    ethnicities = get_option("ethnicity_or_culture")
    return get_closest_match(ethnicities, ethnicity, "Ninguna")

def format_disability_condition(disability_condition: str) -> str:
    disabilities = get_option("disability_condition")
    return get_closest_match(disabilities, disability_condition, "Ninguna")

def format_as_title(text: str) -> str:
    text = normalize_string(text)
    small_words = {"de", "y", "en", "a", "el", "la", "los", "las", "del", "al", "con"}
    words = text.split()
    if len(words) < 2:
        return text.capitalize()
    capitalized_words = [words[0].capitalize()]
    for word in words[1:]:
        if word not in small_words:
            word = word.capitalize()
        capitalized_words.append(word)
    return ' '.join(capitalized_words)

def format_language_level(level: str) -> str:
    old_format_transform = {
        "No lo hablo": "No lo habla",
        "Principiante (A0)": "A0",
        "Básico (A1)": "A1",
        "Básico Alto (A2)": "A2",
        "Intermedio (B1)": "B1",
        "Intermedio-Alto (B2)": "B2",
        "Avanzado(C1)": "C1",
        "Avanzado Alto (C2)": "C2"
    }
    old_format_key = get_closest_match(list(old_format_transform.keys()), level)
    return old_format_transform.get(old_format_key, "No lo habla")

def format_degree(degree: str) -> str:
    degree_levels = get_option("degree")
    return get_closest_match(degree_levels, degree)

def format_degree_status(status: str) -> str:
    degree_levels = get_option("degree_status")
    return get_closest_match(degree_levels, status)

def format_linkedin(link: str) -> str:
    if not ("https" in link.lower() or "www" in link.lower()):
        return ""
    link = link.replace("https://", "")
    link = link.replace("http://", "")
    link = link.replace("www.", "")
    link = link.replace("co.", "")
    if link.endswith("/"):
        link = link[:-1]
    link = link.split("?")[0]
    link = urllib.parse.unquote(link)
    if "/in/" not in link.lower():
        return ""
    return "https://www." + link.strip()

def format_mv_program(program: str) -> str:
    programs_list = get_option("mv_program")
    return get_closest_match(programs_list, program)

def format_occupation(occupation: str) -> str:
    occupations_list = get_option("occupation")
    return get_closest_match(occupations_list, occupation, occupation)

def format_sector(sector: str) -> str:
    sectors_list = get_option("sector")
    sector = sector.replace("Sector ", "")
    return get_closest_match(sectors_list, sector)

def format_role(role: str) -> str:
    roles_list = get_option("role")
    return get_closest_match(roles_list, role)

def format_experience(experience: str) -> str:
    exp_list = get_option("experience_duration")
    return get_closest_match(exp_list, experience)

def format_bool_field(field: str) -> str:
    options = get_option("bool")
    return get_closest_match(options, field, "No")

def get_file_extension(file: str) -> str:
    _, ext = os.path.splitext(file)
    return ext

def int_to_base62(number):
    BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if number == 0:
        return BASE62_ALPHABET[0]
    base62 = []
    while number:
        number, remainder = divmod(number, 62)
        base62.append(BASE62_ALPHABET[remainder])
    return ''.join(reversed(base62))

def hash_to_base62(hash_bytes, length=12):
    number = int.from_bytes(hash_bytes, 'big')
    base62_string = int_to_base62(number)
    return base62_string[:length]

def generate_unique_id() -> str:
    """Generar un id único"""
    timestamp = str(int(time.time() * 1e9)).encode('utf-8')
    random_bytes = secrets.token_bytes(8)  # 8 bytes para mayor entropía
    data_to_hash = timestamp + random_bytes
    hash_object = hashlib.sha256(data_to_hash)
    hash_bytes = hash_object.digest()
    unique_id = hash_to_base62(hash_bytes)
    return unique_id

def generate_deterministic_id(number: str, length=12):
    number = str(number)
    number = number.replace(" ", "")
    number_bytes = number.encode('utf-8')
    hash_object = hashlib.sha256(number_bytes)
    hash_bytes = hash_object.digest()
    unique_id = hash_to_base62(hash_bytes, length)
    return unique_id

def format_file_name_with_id(id: str, prefix: str, ext: str) -> str:
    if ext == "":
        return ""
    new_file_name = prefix + "-" + id + ext
    return new_file_name


def get_name_id(name: str) -> str:
    if not name:
        return "profile"
    parts = [normalize_string(n) for n in name.split(" ")]
    name_id = ""
    for p in parts[:-1]:
        if not p:
            break
        name_id += p[0]
    name_id += parts[-1]
    return name_id
