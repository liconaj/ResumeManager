from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt, Slot
from PySide6.QtWidgets import QWidget, QDialog

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from widgets_controller import LineEditController

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
        self.setup_options()
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
    
    def setup_options(self) -> None:
        self.full_name = LineEditController(self.form.fullNameLineEdit, self.data, "full_name")
        self.email = LineEditController(self.emailLineEdit, self.data, "email")

    @Slot()
    def next_page(self) -> None:
        self.change_page(1)
    
    @Slot()
    def previous_page(self) -> None:
        self.change_page(-1)
    