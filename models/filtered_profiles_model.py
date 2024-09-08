from PySide6.QtCore import QSortFilterProxyModel, QRegularExpression, Qt

class FilteredProfilesModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_column = 0
        self.filer_role = Qt.DisplayRole

    def setFilterColumn(self, column: int):
        self.filter_column = column

    def setFilterRegEx(self, expression: QRegularExpression):
        self.setFilterRegularExpression(expression)
        self.setFilterKeyColumn(self.filter_column)
    
    def setFilterRegExColumn(self, expression: QRegularExpression, column):
        self.filter_column = column
        self.setFilterRegularExpression(expression)
        self.setFilterKeyColumn(column)

    def filterAcceptsRow(self, source_row, source_parent):
        regex = self.filterRegularExpression()
        if not regex.pattern():
            return True
        source_model = self.sourceModel()
        index = source_model.index(source_row, self.filter_column, source_parent)
        value = source_model.data(index, self.filer_role) # Valor de la celda
        matches = regex.match(str(value))
        return matches.hasMatch()
