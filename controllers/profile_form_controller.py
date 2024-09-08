from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt, Slot
from PySide6.QtWidgets import QWidget, QDialog, QComboBox

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from widgets_controller import ComboBoxController, LineEditController, PlainTextEditController

from utils.functions import get_option
from utils.db_manager import DbManager

class ProfileFormController(QDialog):
    def __init__(self, db_manager: DbManager, id: int) -> None:
        super().__init__()
        self.id = id
        self.db_manager = db_manager
        self.data = self.db_manager.get_profile_by_id(id).copy()
        self.form = self.load_ui()
        self.setup_profile_title()
        self.setFixedSize(self.form.size())
        self.setup_stacked_widget()
        self.setup_navigation_buttons()
        self.setup_data_buttons()
        self.setup_line_edits()
        self.setup_plain_texts()
        self.setup_comboboxes()
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
    
    def setup_line_edits(self) -> None:
        self.full_name = LineEditController(self.form.fullNameLineEdit, self.data, "full_name")
        self.email = LineEditController(self.form.emailLineEdit, self.data, "email")
        self.phone = LineEditController(self.form.phoneLineEdit, self.data, "phone")
        self.other_phone = LineEditController(self.form.otherPhoneLineEdit, self.data, "other_phone")
        self.id_num = LineEditController(self.form.idNumLineEdit, self.data, "id_document_number")
        self.id_num_confirm = LineEditController(self.form.idNumConfirmLineEdit, self.data, "id_document_number_confirmation")
        self.under_degree = LineEditController(self.form.underDegreeLineEdit, self.data, "undergraduate_degree")
        self.under_institution = LineEditController(self.form.underInstitutionLineEdit, self.data, "undergraduate_institution")
        self.degree_1_name = LineEditController(self.form.deg1NameLineEdit, self.data, "degree_1_name")
        self.degree_2_name = LineEditController(self.form.deg2NameLineEdit, self.data, "degree_2_name")
        self.degree_3_name = LineEditController(self.form.deg3NameLineEdit, self.data, "degree_3_name")
        self.linkedin = LineEditController(self.form.linkedInLineEdit, self.data, "linkedin")
        self.company = LineEditController(self.form.companyLineEdit, self.data, "company")
    
    def setup_plain_texts(self) -> None:
        self.professional_profile = PlainTextEditController(self.form.professionalProfilePlainTextEdit, self.data, "professional_profile")
        self.role_description = PlainTextEditController(self.form.roleDescriptionPlainTextEdit, self.data, "role_description")
    
    def _setup_combobox(self, combobox: QComboBox, column: str, option: str = None) -> ComboBoxController:
        option = column if option is None else option
        controller = ComboBoxController(combobox, get_option(option), self.data, column)
        return controller

    def setup_comboboxes(self) -> None:
        self.id_type = self._setup_combobox(self.form.idTypeComboBox, "id_document_type")
        self.disability = self._setup_combobox(self.form.disabilityComboBox, "disability_condition")
        self.english = self._setup_combobox(self.form.englishComboBox, "english_level", "language_level")
        self.french = self._setup_combobox(self.form.frenchComboBox, "french_level", "language_level")
        self.portuguese = self._setup_combobox(self.form.portugueseComboBox, "portuguese_level", "language_level")
        self.other_languages = self._setup_combobox(self.form.otherLanguagesComboBox, "other_languages_level", "language_level")
        self.degree_1 = self._setup_combobox(self.form.deg1LevelComboBox, "degree_1", "degree")
        self.degree_1_status = self._setup_combobox(self.form.deg1StatusComboBox, "degree_1_status", "degree_status")
        self.degree_2 = self._setup_combobox(self.form.deg2LevelComboBox, "degree_2", "degree")
        self.degree_2_status = self._setup_combobox(self.form.deg2StatusComboBox, "degree_2_status", "degree_status")
        self.degree_3 = self._setup_combobox(self.form.deg3LevelComboBox, "degree_3", "degree")
        self.degree_3_status = self._setup_combobox(self.form.deg3StatusComboBox, "degree_3_status", "degree_status")
        self.mv_program_1 = self._setup_combobox(self.form.mv1NameComboBox, "mv_program_1", "mv_program")
        self.mv_program_2 = self._setup_combobox(self.form.mv2NameComboBox, "mv_program_2", "mv_program")
        self.mv_program_3 = self._setup_combobox(self.form.mv3NameComboBox, "mv_program_3", "mv_program")
        self.sector = self._setup_combobox(self.form.sectorComboBox, "sector")
        self.role = self._setup_combobox(self.form.roleComboBox, "role")
        self.experience_sector = self._setup_combobox(self.form.expSectorComboBox, "experience_sector", "sector")
        self.experience_duration = self._setup_combobox(self.form.expYearsComboBox, "experience_duration")

    @Slot()
    def next_page(self) -> None:
        self.change_page(1)
    
    @Slot()
    def previous_page(self) -> None:
        self.change_page(-1)
    