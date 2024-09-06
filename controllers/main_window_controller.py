from PySide6.QtCore import Slot, QItemSelectionModel, QRegularExpression
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIntValidator
from models import ProfilesTableModel, FilteredProfilesModel
from utils import DbManager

class MainWindowController(QMainWindow):
    column_widths = [15, 130, 200, 10, 200, 150, 200, 150]

    def __init__(self, window, db_manager: DbManager):
        super().__init__()
        self.window = window
        self.db_manager = db_manager
        profiles_data = self.db_manager.fetch_profiles()
        self.profiles_model = ProfilesTableModel(profiles_data)
        self.filtered_profiles_model = FilteredProfilesModel()
        self.filtered_profiles_model.setSourceModel(self.profiles_model)
        self.setup_table()
        self.setup_see_button()
        self.setup_delete_button()
        self.setup_results_label()
        self.setup_id_search_entry()
        self.adjust_column_widths()
        self.update_results_label()
    
    def setup_see_button(self):
        self.window.seeProfilePushButton.setEnabled(False)
    
    def setup_delete_button(self):
        self.window.deleteProfilePushButton.setEnabled(False)
    
    def setup_table(self):
        self.window.profilesTableView.setModel(self.filtered_profiles_model)
        self.window.profilesTableView.resizeColumnsToContents()
        self.window.profilesTableView.selectionModel().selectionChanged.connect(self.on_selection_changed)
    
    def setup_results_label(self):
        self.filtered_profiles_model.modelReset.connect(self.update_results_label)
        self.filtered_profiles_model.rowsInserted.connect(self.update_results_label)
        self.filtered_profiles_model.rowsRemoved.connect(self.update_results_label)

    def setup_id_search_entry(self):
        validator = QIntValidator()
        self.window.idSearchLineEdit.setValidator(validator)
        self.window.idSearchLineEdit.textChanged.connect(self.on_id_search_text_changed)

    def adjust_column_widths(self):
        for i in range(len(self.column_widths)):
            self.window.profilesTableView.setColumnWidth(i, self.column_widths[i])
    
    @Slot(QItemSelectionModel)
    def on_selection_changed(self, selected, deselected):
        if self.window.profilesTableView.selectionModel().hasSelection():
            self.window.seeProfilePushButton.setEnabled(True)
        else:
            self.window.seeProfilePushButton.setEnabled(False)

    @Slot()
    def on_id_search_text_changed(self, text):
        text = str(int(text)) if text else ""
        filter_pattern = QRegularExpression(text, QRegularExpression.CaseInsensitiveOption)
        self.filtered_profiles_model.setFilterRegExColumn(filter_pattern, 0)
        selection_model = self.window.profilesTableView.selectionModel()
        selection_model.clearSelection()
        if self.filtered_profiles_model.rowCount() > 0:
            index = self.filtered_profiles_model.index(0, 0)
            selection_model.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
            
    
    @Slot()
    def update_results_label(self):
        total_rows = self.profiles_model.rowCount()
        visible_rows = self.window.profilesTableView.model().rowCount()
        text = f"Mostrando {visible_rows} de {total_rows} elementos"
        self.window.resultsLabel.setText(text)