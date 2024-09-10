import datetime
import pandas as pd
import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

def get_flag(row: list) -> str:
    ""
    flag = ""
    if utils.normalize_string(row[9]) != utils.normalize_string(row[10]):
        flag = "IDDOC_UNMATCH"
    return flag

class ExcelProcessor:
    def __init__(self, input_filename):
        self.df = pd.read_excel(input_filename)
    
    def convert_row(self, row) -> dict:
        row_list = row.tolist()
        for i in range(len(row_list)):
            if str(row_list[i]) == "nan":
                row_list[i] = ""
                continue
            if type(row_list[i]) == float:
                try:
                    row_list[i] = int(row_list[i])
                except:
                    print(f"An exception on column {i}")
            elif type(row_list[i]) == datetime.datetime:
                try:
                    row_list[i] = row_list[i].strftime("%d/%m/%Y")
                except:
                    row_list[i] = "1/1/1111"
            row_list[i] = str(row_list[i])
        
        row_converted = {
            "id": row.name,
            "email_form": row_list[0].strip(),
            "authorize_contact": utils.format_bool_field(row_list[1]),
            "authorize_participation": utils.format_bool_field(row_list[2]),
            "motivations": utils.format_motivations(row_list[3]),
            "professional_profile": row_list[4].strip(),
            "full_name": utils.format_as_title(row_list[5]),
            "birth_date": row_list[6].strip(),
            "age": "",
            "id_document_type": utils.format_identity_document_type(row_list[8].strip()),
            "id_document_number": utils.normalize_string(row_list[9]).replace(" ", ""),
            "id_document_number_confirmation": utils.normalize_string(row_list[10]).replace(" ", ""),
            "phone": utils.normalize_string(row_list[11]),
            "other_phone": utils.normalize_string(row_list[12]),
            "email": row_list[13].strip(),
            "birth_department": utils.format_place(row_list[14], row_list[15])[0],
            "birth_municipality": utils.format_place(row_list[14], row_list[15])[1],
            "residence_department": utils.format_place(row_list[16], row_list[17])[0],
            "residence_municipality": utils.format_place(row_list[16], row_list[17])[0],
            "gender": utils.format_gender(row_list[18]),
            "ethnicity_or_culture": utils.format_ethnicity(row_list[19]),
            "disability_condition": utils.format_disability_condition(row_list[21]),
            "undergraduate_degree": row_list[22].strip(),
            "undergraduate_institution": row_list[23].strip(),
            "english_level": utils.format_language_level(row_list[24]),
            "french_level": "No lo habla",
            "portuguese_level": "No lo habla",
            "other_languages_level": utils.format_language_level(row_list[25]),
            "has_degree": utils.format_bool_field(row_list[26]),
            "degree_1": utils.format_degree(row_list[27]),
            "degree_1_name": row_list[28].strip(),
            "degree_1_status": utils.format_degree_status(row_list[29]),
            "degree_2": utils.format_degree(row_list[31]),
            "degree_2_name": row_list[32].strip(),
            "degree_2_status": utils.format_degree_status(row_list[33]),
            "degree_3": utils.format_degree(row_list[35]),
            "degree_3_name": row_list[36].strip(),
            "degree_3_status": utils.format_degree_status(row_list[37]),
            "linkedin": utils.format_linkedin(row_list[39]),
            "mv_participation": utils.format_bool_field(row_list[40]),
            "mv_program_1": utils.format_mv_program(row_list[41]),
            "mv_program_1_year": row_list[42].strip(),
            "mv_program_2": utils.format_mv_program(row_list[44]),
            "mv_program_2_year": row_list[45].strip(),
            "mv_program_3": utils.format_mv_program(row_list[47]),
            "mv_program_3_year": row_list[48].strip(),
            "mlk_program": utils.format_bool_field(row_list[49]),
            "fulbright_seminar": utils.format_bool_field(row_list[50]),
            "occupation": utils.format_occupation(row_list[51]),
            "company": row_list[52].strip(),
            "sector": utils.format_sector(row_list[53]),
            "role": utils.format_role(row_list[54]),
            "role_description": row_list[55].strip(),
            "experience_sector": utils.format_sector(row_list[56]),
            "experience_duration": utils.format_experience(row_list[57]),
            "resume_name": None,
            "resume_link": None,
            "photo_name": None,
            "photo_link": None,
            "tag": get_flag(row_list)
        }
        print("Id:", row.name)
        drive_service = utils.DriveService(utils.Config())
        old_cv_url = row_list[61].strip()
        print(old_cv_url)
        cv_ext = drive_service.get_file_extension(old_cv_url)
        old_photo_url = row_list[62].strip()

        name_id = utils.get_name_id(row_converted["full_name"])
        doc_id = utils.generate_deterministic_id(row_converted["id_document_number"])
        cv_name = utils.format_file_name_with_id(doc_id, name_id, cv_ext)
        photo_name = utils.format_file_name_with_id(doc_id, name_id, ".jpg")
        new_cv_url = drive_service.import_resume(old_cv_url, cv_name)
        new_photo_url = drive_service.import_photo(old_photo_url, photo_name)
        row_converted["resume_name"] = cv_name
        row_converted["resume_link"] = new_cv_url
        row_converted["photo_name"] = photo_name
        row_converted["photo_link"] = new_photo_url

        print(cv_name)
        print(photo_name)

        return row_converted

def process_excel_file(input_filename, output_filename):
    processor = ExcelProcessor(input_filename)
    converted_data = []

    for _, row in processor.df.iterrows():
        converted_data.append(processor.convert_row(row))

    converted_df = pd.DataFrame(converted_data)
    converted_df.to_excel(output_filename, index=False)

#if __name__ == "__main__":
#   parser = argparse.ArgumentParser(description="Procesar archivos de entrada y salida.")
#    parser.add_argument('input_file', type=str, help="Archivo de entrada")
#    parser.add_argument('output_file', type=str, help="Archivo de salida")
#    args = parser.parse_args()
#    process_excel_file(args.input_file, args.output_file)
process_excel_file("scripts/old-master.xlsx", "scripts/master.xlsx")