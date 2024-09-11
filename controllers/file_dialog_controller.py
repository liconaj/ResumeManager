from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject
import os

class FileDialogController(QObject):
    def __init__(self, file_type: str):
        super().__init__()
        self.file_type = file_type.lower()

    def open_file_dialog(self) -> str:
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog  # Evita usar el diálogo nativo (opcional)

        # Configuramos los filtros basados en el tipo de archivo
        if self.file_type == "image":
            file_filter = "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        elif self.file_type == "document":
            file_filter = "Documents (*.pdf *.doc *.docx *.txt)"
        else:
            file_filter = "All Files (*.*)"  # Si no se reconoce el tipo, mostrar todos los archivos

        user_home_dir = os.path.expanduser("~")

        # Abrir el diálogo y permitir seleccionar un archivo
        file_name, _ = QFileDialog.getOpenFileName(
            None, "Select File", user_home_dir, file_filter
        )

        return file_name  # Retorna la ruta del archivo seleccionado o una cadena vacía si se cancela
