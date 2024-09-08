from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Slot
from PySide6.QtWidgets import QDialog, QComboBox, QLineEdit, QFrame, QLabel

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from controllers.fields_controller import *

from utils.functions import get_option, match, open_link, gen_list_of_years
from utils.db_manager import DbManager

class ProfileFormController(QDialog):
    def __init__(self, db_manager: DbManager, id: int) -> None:
        super().__init__()
        self.id = id
        self.db_manager = db_manager
        self.data = self.db_manager.get_profile_by_id(id).copy()
        self.form = self.load_ui()
        self.setFixedSize(self.form.size())

        self.setup_profile_title()
        self.setup_labels()
        self.setup_buttons()
        self.setup_birth_date()
        self.setup_stacked_widget()
        self.setup_navigation_buttons()
        self.setup_data_buttons()
        self.setup_line_edits()
        self.setup_plain_texts()
        self.setup_comboboxes()
        self.setup_radio_buttons_frames()
        self.setup_checkboxes_frame()
        self.update_navigation_buttons()
        self.setWindowTitle("Editar perfil")
    
    def setup_profile_title(self):
        self.form.idLabel.setText(str(self.data["id"]).zfill(3))
        self.form.nameLabel.setText(self.data["full_name"])

    def load_ui(self):
        ui_file_name = "ui/profile_form.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            raise Exception(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        loader = QUiLoader()
        form = loader.load(ui_file, self)
        ui_file.close()
        return form
    
    def setup_stacked_widget(self) -> None:
        self.current_page_index = 0
        self.form.stackedWidget.setCurrentIndex(self.current_page_index)
    
    def setup_navigation_buttons(self) -> None:
        self.form.previousPagePushButton.clicked.connect(self.previous_page)
        self.form.nextPagePushButton.clicked.connect(self.next_page)

    def setup_data_buttons(self) -> None:
        self.form.savePushButton.setEnabled(False)
        self.form.discardPushButton.setEnabled(False)

    def setup_labels(self) -> None:
        forms_email = self.data["email_form"]
        if forms_email:
            self.form.formsEmailLabel.setText(forms_email)

    def setup_buttons(self) -> None:
        self.photo_button = PlainPushButtonController(self.form.photoPushButton, self.data, "photo_name", "photo_link")
        self.resume_button = PlainPushButtonController(self.form.resumePushButton, self.data, "resume_name", "resume_link")
        self.form.seeLinkedInPushButton.clicked.connect(lambda : open_link(self.data["linkedin"]))

    def show(self) -> None:
        self.exec()
    
    def change_page(self, dir: int) -> None:
        self.current_page_index += dir
        self.form.stackedWidget.setCurrentIndex(self.current_page_index)
        self.update_navigation_buttons()
    
    def update_navigation_buttons(self) -> None:
        self.form.previousPagePushButton.setEnabled(self.current_page_index > 0)
        self.form.nextPagePushButton.setEnabled(self.current_page_index < self.form.stackedWidget.count() - 1)
        self.form.navigationLabel.setText(f"Página {self.current_page_index + 1} de {self.form.stackedWidget.count()}")
    
    def _line_edit(self, line_edit: QLineEdit, column: str) -> LineEditController:
        controller = LineEditController(line_edit, self.data, column)
        return controller

    def setup_line_edits(self) -> None:
        self.full_name = self._line_edit(self.form.fullNameLineEdit, "full_name")
        self.email = self._line_edit(self.form.emailLineEdit, "email")
        self.phone = self._line_edit(self.form.phoneLineEdit, "phone")
        self.other_phone = self._line_edit(self.form.otherPhoneLineEdit, "other_phone")
        self.id_num = self._line_edit(self.form.idNumLineEdit, "id_document_number")
        self.id_num_confirm = self._line_edit(self.form.idNumConfirmLineEdit, "id_document_number_confirmation")
        self.under_degree = self._line_edit(self.form.underDegreeLineEdit, "undergraduate_degree")
        self.under_institution = self._line_edit(self.form.underInstitutionLineEdit, "undergraduate_institution")
        self.degree_1_name = self._line_edit(self.form.deg1NameLineEdit, "degree_1_name")
        self.degree_2_name = self._line_edit(self.form.deg2NameLineEdit, "degree_2_name")
        self.degree_3_name = self._line_edit(self.form.deg3NameLineEdit, "degree_3_name")
        self.linkedin = self._line_edit(self.form.linkedInLineEdit, "linkedin")
        self.company = self._line_edit(self.form.companyLineEdit, "company")
    
    def setup_plain_texts(self) -> None:
        self.professional_profile = PlainTextEditController(self.form.professionalProfilePlainTextEdit, self.data, "professional_profile")
        self.role_description = PlainTextEditController(self.form.roleDescriptionPlainTextEdit, self.data, "role_description")
    
    def _combobox(self, combobox: QComboBox, column: str, option: str = None) -> ComboBoxController:
        option = column if option is None else option
        controller = ComboBoxController(combobox, get_option(option), self.data, column)
        return controller

    def setup_comboboxes(self) -> None:
        self.id_type = self._combobox(self.form.idTypeComboBox, "id_document_type")
        self.disability = self._combobox(self.form.disabilityComboBox, "disability_condition")
        self.english = self._combobox(self.form.englishComboBox, "english_level", "language_level")
        self.french = self._combobox(self.form.frenchComboBox, "french_level", "language_level")
        self.portuguese = self._combobox(self.form.portugueseComboBox, "portuguese_level", "language_level")
        self.other_languages = self._combobox(self.form.otherLanguagesComboBox, "other_languages_level", "language_level")
        self.degree_1 = self._combobox(self.form.deg1LevelComboBox, "degree_1", "degree")
        self.degree_1_status = self._combobox(self.form.deg1StatusComboBox, "degree_1_status", "degree_status")
        self.degree_2 = self._combobox(self.form.deg2LevelComboBox, "degree_2", "degree")
        self.degree_2_status = self._combobox(self.form.deg2StatusComboBox, "degree_2_status", "degree_status")
        self.degree_3 = self._combobox(self.form.deg3LevelComboBox, "degree_3", "degree")
        self.degree_3_status = self._combobox(self.form.deg3StatusComboBox, "degree_3_status", "degree_status")
        self.mv_program_1 = self._combobox(self.form.mv1NameComboBox, "mv_program_1", "mv_program")
        self.mv_program_2 = self._combobox(self.form.mv2NameComboBox, "mv_program_2", "mv_program")
        self.mv_program_3 = self._combobox(self.form.mv3NameComboBox, "mv_program_3", "mv_program")
        self.occupation = self._combobox(self.form.occupationComboBox, "occupation")
        self.sector = self._combobox(self.form.sectorComboBox, "sector")
        self.role = self._combobox(self.form.roleComboBox, "role")
        self.experience_sector = self._combobox(self.form.expSectorComboBox, "experience_sector", "sector")
        self.experience_duration = self._combobox(self.form.expYearsComboBox, "experience_duration")
        self.birth_place = PlaceComboBoxesController(self.form.birthDeptComboBox, "birth_department",
            self.form.birthCityComboBox, "birth_municipality", self.data)
        self.residence_place = PlaceComboBoxesController(self.form.residenceDeptComboBox, "residence_department",
            self.form.residenceCityComboBox, "residence_municipality", self.data)
        mv_years = gen_list_of_years(2010)
        self.mv_year_1 = ComboBoxController(self.form.mv1YearComboBox, mv_years, self.data, "mv_program_1_year")
        self.mv_year_2 = ComboBoxController(self.form.mv2YearComboBox, mv_years, self.data, "mv_program_2_year")
        self.mv_year_3 = ComboBoxController(self.form.mv3YearComboBox, mv_years, self.data, "mv_program_3_year")

    def _radio_buttons_frame(self, frame: QFrame, column: str, option: str = None) -> RadioButtonsFrameController:
        option = column if option is None else option
        controller = RadioButtonsFrameController(frame, get_option(option), self.data, column)
        return controller
    
    def setup_radio_buttons_frames(self) -> None:
        self.contact_frame = self._radio_buttons_frame(self.form.contactFrame, "authorize_contact", "bool")
        self.participation_frame = self._radio_buttons_frame(self.form.participationFrame, "authorize_participation", "bool")
        self.gender_frame = self._radio_buttons_frame(self.form.genderFrame, "gender")
        self.ethnicity_frame = self._radio_buttons_frame(self.form.ethnicityFrame, "ethnicity_or_culture")
        self.degrees_frame = self._radio_buttons_frame(self.form.degreesFrame, "has_degree", "bool")
        self.degrees_frame.toggled_connect(lambda: self.toggle_subframes(self.degrees_frame))
        self.mv_frame = self._radio_buttons_frame(self.form.mvFrame, "mv_participation", "bool")
        self.mv_frame.toggled_connect(lambda: self.toggle_subframes(self.mv_frame))
        self.mlk_frame = self._radio_buttons_frame(self.form.mlkFrame, "mlk_program", "bool")
        self.fulbright_seminar = self._radio_buttons_frame(self.form.fulbrightFrame, "fulbright_seminar", "bool")

    def setup_checkboxes_frame(self) -> None:
        self.motivations = CheckBoxesFrameController(self.form.motivationsFrame, get_option("motivations"), self.data, "motivations")
    
    def setup_birth_date(self) -> None:
        self.birth_date = DateEditController(self.form.birthDateEdit, self.data, "birth_date")
        self.birth_date.date_changed.connect(self.update_age)
        self.update_age(self.birth_date.date())
    
    def toggle_subframes(self, radio_buttons_frame: RadioButtonsFrameController, enable_value = "Si") -> None:
        selected_option = radio_buttons_frame.selected_option()
        should_enable = match(selected_option, enable_value)
        for widget in radio_buttons_frame.frame.children():
            if isinstance(widget, QFrame) and not isinstance(widget, QLabel):
                widget.setEnabled(should_enable)

    @Slot()
    def next_page(self) -> None:
        self.change_page(1)
    
    @Slot(QDate)
    def update_age(self, date_of_birth: QDate) -> None:
        today = QDate.currentDate()
        age = today.year() - date_of_birth.year()
        if (today.month() < date_of_birth.month()) or \
           (today.month() == date_of_birth.month() and today.day() < date_of_birth.day()):
            age -= 1
        self.form.ageLabel.setText(f"{age} años")
    
    @Slot()
    def previous_page(self) -> None:
        self.change_page(-1)
    