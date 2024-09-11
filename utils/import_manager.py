import os
import sys
from typing import Any

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import utils.functions as f
from utils.config import Config
from utils.gspreadsheet import GSpreadSheet
from utils.db_manager import DbManager


_no_format = lambda x : x
_fields_format_functions = {
    "email_form": _no_format,
    "authorize_contact": f.format_bool_field,
    "authorize_participation": f.format_bool_field,
    "motivations": f.format_motivations,
    "professional_profile": _no_format,
    "full_name": f.format_as_title,
    "birth_date": _no_format,
    "id_document_type": f.format_identity_document_type,
    "id_document_number": _no_format,
    "id_document_number_confirmation": _no_format,
    "phone": _no_format,
    "other_phone": _no_format,
    "email": _no_format,
    "birth_department": _no_format,
    "birth_municipality": _no_format,
    "residence_department": _no_format,
    "residence_municipality": _no_format,
    "gender": f.format_gender,
    "ethnicity_or_culture": f.format_ethnicity,
    "disability_condition": f.format_disability_condition,
    "undergraduate_degree": _no_format,
    "undergraduate_institution": _no_format,
    "english_level": f.format_language_level,
    "french_level": f.format_language_level,
    "portuguese_level": f.format_language_level,
    "other_languages_level": f.format_language_level,
    "has_degree": f.format_bool_field,
    "degree_1": f.format_degree,
    "degree_1_name": _no_format,
    "degree_1_status": f.format_degree_status,
    "degree_2": f.format_degree,
    "degree_2_name": _no_format,
    "degree_2_status": f.format_degree_status,
    "degree_3": f.format_degree,
    "degree_3_name": _no_format,
    "degree_3_status": f.format_degree_status,
    "linkedin": f.format_linkedin,
    "mv_participation": f.format_bool_field,
    "mv_program_1": f.format_mv_program,
    "mv_program_1_year": _no_format,
    "mv_program_2": f.format_mv_program,
    "mv_program_2_year": _no_format,
    "mv_program_3": f.format_mv_program,
    "mv_program_3_year": _no_format,
    "mlk_program": f.format_bool_field,
    "fulbright_seminar": f.format_bool_field,
    "occupation": f.format_occupation,
    "company": _no_format,
    "sector": f.format_sector,
    "role": f.format_role,
    "role_description": _no_format,
    "experience_sector": f.format_sector,
    "experience_duration": f.format_experience,
    "resume_link": _no_format,
    "photo_link": _no_format,
    "tag": _no_format
}

class ImportManager:
    def __init__(self, config: Config, db_manager: DbManager) -> None:
        self.import_config = None
        self.config = config
        self.db_manager = db_manager
        self.imported_profiles = self.db_manager.fetch_profiles()

    def _import_forms(self) -> list[dict[str, Any]]:
        return self.config.get("IMPORT_FORM")
    
    def _get_form_config(self, index: int) -> dict[str, Any]:
        return self._import_forms()[index]
    
    def _get_field(self, field, row: list[Any]) -> str:
        columns = self.import_config[field]
        if type(columns) != list:
            columns = (int(columns), int(columns))
        start, end = columns
        for i in range(start, end+1):
            if i >= len(row):
                return ""
            info = row[i].strip()
            if info:
                return info
        return ""
    
    def _get_profile_unique_id(self, profile: dict[str, str]) -> bool:
        name_id = f.get_name_id(profile["full_name"])
        unique_id = f.generate_deterministic_id(profile["id_document_type"])
        return f"{name_id}-{unique_id}"
    
    def _is_already_imported(self, profile: dict[str, str]) -> bool:
        profile_unique_id = self._get_profile_unique_id(profile)
        
        for p in self.imported_profiles:
            if self._get_profile_unique_id(p) == profile_unique_id:
                return True
        return False
    
    def _format_profile(self, row: list[Any]) -> dict[str, str]:
        profile = dict()
        for field, format_function in _fields_format_functions.items():
            profile[field] = format_function(self._get_field(field, row))
        birth_department, birth_city = f.format_place(profile["birth_department"], profile["birth_municipality"])
        recidence_department, recidence_city = f.format_place(profile["residence_department"], profile["residence_municipality"])
        profile["birth_department"] = birth_department
        profile["birth_municipality"] = birth_city
        profile["residence_department"] = recidence_department
        profile["residence_municipality"] = recidence_city
        profile["_already_imported"] = self._is_already_imported(profile)
        return profile

    def set_import_form(self, index: int) -> dict[str, Any]:
        self.import_config = self._get_form_config(index)
    
    def get_forms_names(self) -> list[str]:
        names = []
        for fconf in self._import_forms():
            names.append(fconf.get("_name", ""))
        return names
    
    def get_form_profiles(self) -> list[dict[str, str]]:
        sheet_id = self.import_config["_sheet_id"]
        range_name = self.import_config["_range_name"]
        sheet = GSpreadSheet(sheet_id, range_name)
        rows = sheet.get_raw_data()[1:]
        return [self._format_profile(p) for p in rows]
    