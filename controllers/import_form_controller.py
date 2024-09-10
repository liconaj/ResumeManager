from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QObject, Qt, Slot, Signal
from PySide6.QtWidgets import QDialog, QComboBox, QTableView, QPushButton
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtCore import QSortFilterProxyModel
from typing import Any

import os
import sys

from utils.functions import format_file_name_with_id, generate_deterministic_id, get_name_id

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from message_box_controller import MessageBoxController

from utils import ImportManager, DbManager, Config, DriveService


_display_headers = [
    "tag",
    "full_name", "id_document_type", "id_document_number", "birth_date",
    "phone", "email", "gender", "ethnicity_or_culture", "occupation",
    "undergraduate_degree", "undergraduate_institution",
    "degree_1", "degree_1_name", "degree_1_status",
    "degree_2", "degree_2_name", "degree_2_status",
    "degree_3", "degree_3_name", "degree_3_status",
    "mv_program_1", "mv_program_1_year",
    "mv_program_2", "mv_program_2_year",
    "mv_program_3", "mv_program_3_year",
]

class TableModel(QAbstractTableModel):
    def __init__(self, data: list[dict[str, Any]],  parent = None) -> None:
        super().__init__(parent)
        self._headers = _display_headers
        self.load_data(data)
        
        
    def load_headers(self, data: list[dict[str, Any]]):
        self._headers = []
        for h in data[0]:
            if h.startswith("_"):
                continue
            self._headers.append(h)
    
    def load_data(self, data: list[dict[str, Any]]):
        self._data = []
        for item in data:
            row = [item[h] for h in self._headers]
            self._data.append(row)
    
    def data(self, index: QModelIndex, role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self._data[row][column]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._data[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            if orientation == Qt.Vertical:
                return section + 1
        return None
    
    def clear(self):
        self._headers = []
        self._data = []


class ImportFormController(QDialog):
    def __init__(self, db_manager: DbManager, config: Config) -> None:
        super().__init__()
        self.no_imported_table = None
        self.db_manager = db_manager
        self.config = config
        self.import_manager = ImportManager(config, db_manager)
        self.form = self.load_ui()
        self.setup_import_from()
        self.setFixedSize(self.form.size())
        self.setWindowTitle("Importar perfil")
    
    def load_ui(self):
        ui_file_name = "ui/import_form.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            raise Exception(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        loader = QUiLoader()
        form = loader.load(ui_file, self)
        ui_file.close()
        return form
    
    def show(self) -> None:
        self.exec()
    
    def load_profiles(self) -> None:
        index = self.import_from.currentIndex()
        self.import_manager.set_import_form(index)
        all_profiles = self.import_manager.get_form_profiles()
        self.no_imported_profiles = []
        self.already_imported_profiles = []
        for p in all_profiles:
            if not p["id_document_type"] or not p["full_name"]:
                continue
            if p["_already_imported"]:
                self.already_imported_profiles.append(p)
            else:
                self.no_imported_profiles.append(p)
    
    def get_selected_no_imported_profile_index(self) -> dict[str,str] | None:
        if not self.no_imported_table:
            return None
        selected_index = self.no_imported_table.selectionModel().currentIndex()
        if not selected_index.isValid():
            return None
        original_index = self.no_imported_model_filter.mapToSource(selected_index)
        return original_index.row()

    def setup_table_views(self) -> None:
        self.no_imported_model = TableModel(self.no_imported_profiles)
        self.no_imported_model_filter = QSortFilterProxyModel()
        self.no_imported_model_filter.setSourceModel(self.no_imported_model)

        self.already_imported_model = TableModel(self.already_imported_profiles)
        self.already_imported_model_filter = QSortFilterProxyModel()
        self.already_imported_model_filter.setSourceModel(self.already_imported_model)

        self.no_imported_table: QTableView = self.form.noImportedTableView
        self.no_imported_table.setModel(self.no_imported_model_filter)
        self.no_imported_table.setSortingEnabled(True)

        self.already_imported_table: QTableView = self.form.alreadyImportedTableView
        self.already_imported_table.setModel(self.already_imported_model_filter)
        self.already_imported_table.setSortingEnabled(True)
    
    def setup_import_from(self) -> None:
        self.import_from: QComboBox = self.form.importFromComboBox
        forms = self.import_manager.get_forms_names()
        self.import_from.addItems(forms)
        self.load: QPushButton = self.form.loadPushButton
        self.load.clicked.connect(self.on_load_clicked)
    
    def setup_import_button(self) -> None:
        self.import_button: QPushButton = self.form.importPushButton
        self.import_button.clicked.connect(self.on_import_clicked)
    
    def setup_sort_by(self) -> None:
        self.sort_by: QComboBox = self.form.sortByComboBox
        self.sort_by.addItems(_display_headers)
        self.sort_by.setCurrentIndex(1)
        self.sort_by.currentIndexChanged.connect(self.on_sort_by_changed)
        self.sort_profiles()
    
    def sort_profiles(self) -> None:
        column = self.sort_by.currentIndex()
        self.no_imported_table.sortByColumn(column, Qt.AscendingOrder)
        self.already_imported_table.sortByColumn(column, Qt.AscendingOrder)


    @Slot()
    def on_load_clicked(self) -> None:
        self.load.setEnabled(False)
        self.load_profiles()
        self.setup_table_views()
        self.setup_sort_by()
        self.setup_import_button()
        self.load.setEnabled(True)
    
    def import_profile(self, profile: dict[str, str]) -> None:
        profile = profile.copy()
        for k in list(profile.keys()):
            if k.startswith("_"):
                del profile[k]
        drive_service = DriveService(self.config)

        resume_ext = drive_service.get_file_extension(profile["resume_link"])
        name_id = get_name_id(profile["full_name"])
        doc_id = generate_deterministic_id(profile["id_document_number"])

        resume_name = format_file_name_with_id(doc_id, name_id, resume_ext)
        photo_name = format_file_name_with_id(doc_id, name_id, ".jpg")
        
        profile["resume_name"] = resume_name
        profile["resume_link"] = drive_service.import_resume(profile["resume_link"], resume_name)
        profile["photo_name"] = photo_name
        profile["photo_link"] = drive_service.import_resume(profile["photo_link"], photo_name)

        self.db_manager.update_local_db_with_profile(profile)
    
    @Slot()
    def on_sort_by_changed(self) -> None:
        self.sort_profiles()
    
    @Slot()
    def on_import_clicked(self) -> None:
        index = self.get_selected_no_imported_profile_index()
        profile = self.no_imported_profiles.pop(index)
        new_tag = "NEW"
        if profile["tag"]:
            new_tag += "+"
        profile["tag"] = new_tag + profile["tag"]
        profile["_already_imported"] = True
        self.already_imported_profiles.append(profile)
        self.setup_table_views()
        self.import_profile(profile)
