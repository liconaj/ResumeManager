from PySide6.QtWidgets import QLineEdit, QPlainTextEdit
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
