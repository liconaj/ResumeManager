from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from typing import Any
from utils import calc_age

_view_headers = {
    "id": "Id",
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
        self.original_data = data
        self._headers = list(_view_headers.values())
        self.load_data()
        
    def load_data(self):
        self._data = []
        for item in self.original_data:
            row = []
            for k in _view_headers:
                if k == "age":
                    value = calc_age(item["birth_date"])
                else:
                    value = str(item[k])
                row.append(value)
            self._data.append(row)
    
    def update_data(self, new_data):
        self.original_data = new_data
        self.load_data()
    
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