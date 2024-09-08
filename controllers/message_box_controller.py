from PySide6.QtWidgets import QMessageBox, QWidget

class MessageBoxController:
    def __init__(self, parent: QWidget, title: str, text: str, yes_func: callable, no_func: callable = lambda : None) -> None:
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        
        yes_button = msg_box.addButton("Sí", QMessageBox.YesRole)
        no_button = msg_box.addButton("No", QMessageBox.NoRole)
        
        msg_box.setDefaultButton(no_button)  # Hacer que "No" sea el predeterminado
        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            yes_func()
        else:
            no_func()
