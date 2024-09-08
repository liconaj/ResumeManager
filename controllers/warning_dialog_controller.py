from PySide6.QtWidgets import QMessageBox

class WarningDialogController:
    def __init__(self, parent=None):
        self.parent = parent

    def show_warning_dialog(self, title: str, message: str):
        warning_dialog = QMessageBox(self.parent)
        warning_dialog.setIcon(QMessageBox.Warning)
        warning_dialog.setWindowTitle(title)
        warning_dialog.setText(message)
        warning_dialog.setStandardButtons(QMessageBox.Ok)
        warning_dialog.exec()
