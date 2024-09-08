from PySide6.QtWidgets import QLineEdit, QPlainTextEdit, QComboBox, QFrame, QRadioButton, QCheckBox, QPushButton
from PySide6.QtCore import Slot
from utils import match, get_closest_match
from utils.functions import normalize_string, open_link

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
        self.null_option = "   "
        self.options = [self.null_option] + options
        self.data_dict = data_dict
        self.key = key
        self.combo_box.addItems(self.options)
        self.placeholder_text = self.combo_box.placeholderText()
        
        current_value = self.data_dict.get(self.key, None)
        if current_value in self.options:
            self.combo_box.setCurrentText(current_value)
        if current_value == self.null_option:
            self.combo_box.setCurrentIndex(-1)
        self.combo_box.currentTextChanged.connect(self.on_selection_changed)

    @Slot(str)
    def on_selection_changed(self, selected_value: str) -> None: 
        if selected_value == self.null_option:
            selected_value = ""
            self.combo_box.setCurrentIndex(-1)
        self.data_dict[self.key] = selected_value

class RadioButtonsFrameController:
    def __init__(self, frame: QFrame, options: list[str], data_dict: dict, key: str) -> None:
        self.frame = frame
        self.options = options
        self.data_dict = data_dict
        self.key = key
        self.radio_buttons = {}
        self.is_bool = False
        if self.options == ["Si", "No"]:
            self.is_bool = True

        current_value = self.data_dict.get(self.key, None)
        closest_value = get_closest_match(self.options, current_value) if current_value else None

        for widget in self.frame.children():
            if isinstance(widget, QRadioButton):
                button_text = widget.text()
                self.radio_buttons[button_text] = widget
                if closest_value and match(button_text, closest_value):
                    widget.setChecked(True)
                widget.toggled.connect(self.on_radio_button_toggled)

    def selected_option(self) -> str:
        for text, radio_button in self.radio_buttons.items():
            if radio_button.isChecked():
                if self.is_bool:
                    text = normalize_string(text).capitalize()
                return get_closest_match(self.options, text, "")
        return ""
    
    def toggled_connect(self, custom_func: callable) -> None:
        custom_func()
        self.toggled_custom_func = custom_func

    @Slot()
    def on_radio_button_toggled(self) -> None:
        self.data_dict[self.key] = self.selected_option()
        if self.toggled_custom_func is not None:
            self.toggled_custom_func()


class CheckBoxesFrameController:
    def __init__(self, frame: QFrame, options: list[str], data_dict: dict, key: str) -> None:
        self.frame = frame
        self.options = options
        self.data_dict = data_dict
        self.key = key
        self.checkboxes = {}

        self.init_checkboxes()
        self.set_initial_state()

    def init_checkboxes(self) -> None:
        all_checkboxes = self.frame.findChildren(QCheckBox)
        for checkbox in all_checkboxes:
            checkbox_text = checkbox.text()
            checkbox_option = get_closest_match(self.options, checkbox_text)
            if checkbox is not None:
                checkbox.stateChanged.connect(self.on_checkbox_state_changed)  # Conectar el slot
                self.checkboxes[checkbox_option] = checkbox

    def set_initial_state(self) -> None:
        current_value = self.data_dict.get(self.key, "")
        selected_options = current_value.split(",") if current_value else []
        for option, checkbox in self.checkboxes.items():
            checkbox.setChecked(option in selected_options)

    @Slot()
    def on_checkbox_state_changed(self) -> None:
        self.update_data()

    def update_data(self) -> None:
        self.data_dict[self.key] = ",".join(self.selected_options())

    def selected_options(self) -> list[str]:
        return [option for option, checkbox in self.checkboxes.items() if checkbox.isChecked()]


class PlainPushButtonController:
    def __init__(self, push_button: QPushButton, data: dict, key, link_key = "") -> None:
        self.push_button = push_button
        self.data = data
        self.key = key
        self.link_key = link_key
        
        self.push_button.clicked.connect(self.on_clicked)
        self.update()

    def update(self) -> None:
        text = self.data[self.key]
        link = self.data[self.link_key].strip()
        if link == "":
            self.push_button.setEnabled(False)
            self.push_button.setText("N/A")
        else:
            self.push_button.setEnabled(True)
            self.push_button.setText(text)
    
    @Slot()
    def on_clicked(self):
        open_link(self.data[self.link_key])