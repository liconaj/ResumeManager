from PySide6.QtWidgets import QLineEdit, QPlainTextEdit, QComboBox
from PySide6.QtCore import Slot

class LineEditController:
    def __init__(self, line_edit: QLineEdit, data: dict, key: str) -> None:
        self.line_edit = line_edit
        self.data_dict = data
        self.key = key
        self.line_edit.setText(self.data_dict.get(self.key, ""))
        self.line_edit.textChanged.connect(self.on_text_changed)
    
    @Slot(str)
    def on_text_changed(self, text: str) -> None:
        self.data_dict[self.key] = text

class PlainTextEditController:
    def __init__(self, plain_text_edit: QPlainTextEdit, data_dict: dict, key: str) -> None:
        self.plain_text_edit = plain_text_edit
        self.data_dict = data_dict
        self.key = key
        self.plain_text_edit.setPlainText(self.data_dict.get(self.key, ""))
        self.plain_text_edit.textChanged.connect(self.on_text_changed)
    
    @Slot()
    def on_text_changed(self) -> None:
        self.data_dict[self.key] = self.plain_text_edit.toPlainText()


class ComboBoxController:
    def __init__(self, combo_box: QComboBox, options: list[str], data_dict: dict, key: str) -> None:
        self.combo_box = combo_box
        self.options = options
        self.data_dict = data_dict
        self.key = key
        self.combo_box.addItems(self.options)
        current_value = self.data_dict.get(self.key, None)
        if current_value in self.options:
            self.combo_box.setCurrentText(current_value)
        self.combo_box.currentTextChanged.connect(self.on_selection_changed)

    @Slot(str)
    def on_selection_changed(self, selected_value: str) -> None: 
        self.data_dict[self.key] = selected_value
