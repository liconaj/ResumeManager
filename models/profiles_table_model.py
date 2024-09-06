from PySide6.QtCore import QAbstractTableModel, QObject, Qt, QModelIndex
from typing import Any

_view_headers = {
    "id": "ID",
    "id_document_number": "Número de identidad",
    "full_name": "Nombres y apellidos",
    "age": "Edad",
    "undergraduate_degree": "Pregrado",
    "ethnicity_or_culture": "Etnia",
    "occupation": "Ocupación",
    "tag": "Etiqueta"
}


class ProfilesTableModel(QAbstractTableModel):
    def __init__(self, data: list[dict[str,Any]], parent=None) -> None:
        super().__init__(parent)
        self._headers = list(_view_headers.values())
        self._data = []
        for item in data:
            self._data.append([item[k] for k in _view_headers])
    
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