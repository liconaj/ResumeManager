from PySide6.QtWidgets import QLineEdit
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
