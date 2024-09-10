from pony.orm import Database, Optional, PrimaryKey, db_session
from typing import Any

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gspreadsheet import GSpreadSheet
from functions import get_abspath_relative_root

FILE_PATH = get_abspath_relative_root("data/database.sqlite")

db = Database()

class Profile(db.Entity):
    id = PrimaryKey(int, auto=True)
    email_form = Optional(str)
    authorize_contact = Optional(str)
    authorize_participation = Optional(str)
    motivations = Optional(str)
    professional_profile = Optional(str)  # Usado 'text' en el caso de largas cadenas
    full_name = Optional(str)
    birth_date = Optional(str)
    age = Optional(int)
    id_document_type = Optional(str)
    id_document_number = Optional(str)
    id_document_number_confirmation = Optional(str)
    phone = Optional(str)
    other_phone = Optional(str)
    email = Optional(str)
    birth_department = Optional(str)
    birth_municipality = Optional(str)
    residence_department = Optional(str)
    residence_municipality = Optional(str)
    gender = Optional(str)
    ethnicity_or_culture = Optional(str)
    disability_condition = Optional(str)
    undergraduate_degree = Optional(str)
    undergraduate_institution = Optional(str)
    english_level = Optional(str)
    french_level = Optional(str)
    portuguese_level = Optional(str)
    other_languages_level = Optional(str)
    has_degree = Optional(str)
    degree_1 = Optional(str)
    degree_1_name = Optional(str)
    degree_1_status = Optional(str)
    degree_2 = Optional(str)
    degree_2_name = Optional(str)
    degree_2_status = Optional(str)
    degree_3 = Optional(str)
    degree_3_name = Optional(str)
    degree_3_status = Optional(str)
    linkedin = Optional(str)
    mv_participation = Optional(str)
    mv_program_1 = Optional(str)
    mv_program_1_year = Optional(str)
    mv_program_2 = Optional(str)
    mv_program_2_year = Optional(str)
    mv_program_3 = Optional(str)
    mv_program_3_year = Optional(str)
    mlk_program = Optional(str)
    fulbright_seminar = Optional(str)
    occupation = Optional(str)
    company = Optional(str)
    sector = Optional(str)
    role = Optional(str)
    role_description = Optional(str)  # Usado 'text' en el caso de largas cadenas
    experience_sector = Optional(str)
    experience_duration = Optional(str)
    resume_name = Optional(str)
    resume_link = Optional(str)
    photo_name = Optional(str)
    photo_link = Optional(str)
    tag = Optional(str)

db.bind(provider='sqlite', filename=FILE_PATH, create_db=True)
db.generate_mapping(create_tables=True)

class DbManager:
    def __init__(self):
        self.gspreadsheet = None

    def set_gspreadsheet(self, gspreadsheet: GSpreadSheet):
        self.gspreadsheet = gspreadsheet

    @db_session
    def synchronize(self):
        if self.gspreadsheet is None:
            raise ValueError("Variable gspreadsheet no establecido")
        self.gspreadsheet.restart_service()
        if not self.gspreadsheet.available:
            print("[DB_MANAGER] No se pudo establecer conexión con la base de datos remota")
            return
    
        # Obtén los datos de Google Sheets como una lista de diccionarios
        sheet_data: list[dict[str, Any]] = self.gspreadsheet.fetch_data()
        local_data = self.fetch_profiles()

        sheet_row_count = len(sheet_data)
        local_row_count = len(local_data)
            
        if local_row_count > sheet_row_count:
            self._update_gspreadsheet_with_local_db()
            print("[DB_MANAGER] Actualizando datos en la nube")
        elif sheet_row_count > local_row_count:
            self._update_local_db_with_gspreadsheet()
            print("[DB_MANAGER] Actualizando datos locales")
        else:
            print("[DB_MANAGER] Base de datos actualizada")

    @db_session
    def _update_local_db_with_gspreadsheet(self):
        data: list[dict[str, Any]] = self.gspreadsheet.fetch_data()
        for item in data:
            profile = Profile.get(id=item.get('id'))
            if not profile:
                Profile(**item)
            else:
                for key, value in item.items():
                    setattr(profile, key, value)
        print("[DB_MANAGER] Numero de entradas:", Profile.select().count())

    @db_session
    def _update_gspreadsheet_with_local_db(self):
        headers = Profile._columns_
        values: list[list[Any]] = [list(headers)] + [[getattr(profile, header, "") for header in headers] for profile in Profile.select()]
        self.gspreadsheet.update_sheet(values)

    @db_session
    def fetch_profiles(self) -> list[dict[str, Any]]:
        return [p.to_dict() for p in Profile.select()]
    
    @db_session
    def get_profile_by_id(self, id: int) -> dict[str, Any]:
        profile = Profile.get(id=id)
        return profile.to_dict() if profile else None
    
    @db_session
    def update_local_db_with_profile(self, profile_data: dict[str, Any]) -> None:
        profile_id = profile_data.get('id', None)
        # Si el ID está presente, intentamos encontrar el perfil
        if profile_id is not None:
            profile = Profile.get(id=int(profile_id))
            if profile:
                # Actualizamos los campos existentes
                for key, value in profile_data.items():
                    if hasattr(profile, key) and key != "id":
                        setattr(profile, key, value)
            else:
                # Si no encontramos el perfil, creamos uno nuevo
                Profile(**profile_data)
        else:
            # Si no hay ID, creamos un nuevo perfil
            Profile(**profile_data)
