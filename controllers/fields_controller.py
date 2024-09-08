import requests
from io import BytesIO
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem
from PySide6.QtCore import Signal, Slot, QDate, QObject, Qt, QThread
from PySide6.QtWidgets import QLineEdit, QPlainTextEdit, QComboBox, QFrame, QRadioButton, QCheckBox, QPushButton, QDateEdit
from utils import match, get_closest_match
from utils.functions import get_option, normalize_string, open_link



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
    def __init__(self, combo_box: QComboBox, options: list[str] | None, data_dict: dict, key: str) -> None:
        self.custom_func = None
        self.combo_box = combo_box
        self.null_option = "   "
        self.data_dict = data_dict
        self.key = key
        self.set_options(options)
        self.combo_box.currentTextChanged.connect(self.on_selection_changed)
    
    def set_options(self, options: list[str] | None) -> None:
        self.options = options
        self.combo_box.clear()
        if options is None:
            self.combo_box.setEnabled(False)
        else:
            self.combo_box.setEnabled(True)
            self.options = [self.null_option] + options
            self.combo_box.addItems(self.options)
        self.update()
        self.combo_box.setMaxVisibleItems = 10
    
    def update(self) -> None:
        if self.options is None:
            return
        current_value = self.data_dict.get(self.key, None)
        if current_value in self.options:
            self.combo_box.setCurrentText(current_value)
        else:
            self.combo_box.setCurrentIndex(-1)
    
    def connect(self, custom_func: callable) -> None:
        self.custom_func = custom_func

    @Slot(str)
    def on_selection_changed(self, selected_value: str) -> None: 
        if selected_value == self.null_option:
            selected_value = ""
            self.combo_box.setCurrentIndex(-1)
        self.data_dict[self.key] = selected_value
        if self.custom_func and selected_value:
            self.custom_func(selected_value)


class PlaceComboBoxesController:
    def __init__(self, dept_combobox: QComboBox, dept_key: str, city_combobox: QComboBox, city_key: str, data_dict: dict) -> None:
        self.data_dict = data_dict
        self.dept_key = dept_key
        self.city_key = city_key
        self.department_cities: dict = get_option("department_cities")
        self.dept_combobox = ComboBoxController(dept_combobox, sorted(list(self.department_cities.keys())), data_dict, dept_key)
        options = self.department_cities.get(data_dict[dept_key], None)
        self.city_combobox = ComboBoxController(city_combobox, sorted(options), data_dict, city_key)
        self.dept_combobox.connect(self.on_dept_selection_changed)
    
    @Slot(str)
    def on_dept_selection_changed(self, selected_value: str) -> None:
        options = self.department_cities.get(selected_value, None)
        self.city_combobox.set_options(sorted(options))


class RadioButtonsFrameController:
    def __init__(self, frame: QFrame, options: list[str], data_dict: dict, key: str) -> None:
        self.toggled_custom_func = None
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


class DateEditController(QObject):
    date_changed = Signal(QDate)

    def __init__(self, date_edit: QDateEdit, data_dict: dict, key: str) -> None:
        super(DateEditController, self).__init__()
        self.date_edit = date_edit
        self.data_dict = data_dict
        self.key = key
        date_str = self.data_dict.get(self.key, "")
        self.date_changed_custom_func = None
        if date_str:
            try:
                day, month, year = map(int, date_str.split("/"))
                date = QDate(year, month, day)
                self.date_edit.setDate(date)
            except ValueError:
                self.date_edit.setDate(QDate.currentDate())  # Establecer fecha actual si hay error
        else:
            self.date_edit.setDate(QDate.currentDate())  # Establecer fecha actual si el valor es vacío
        self.date_edit.dateChanged.connect(self.on_date_changed)
        self.date_changed.emit(self.date_edit.date())
    
    def date(self) -> QDate:
        return self.date_edit.date()

    @Slot(QDate)
    def on_date_changed(self, date: QDate) -> None:
        date_str = date.toString("dd/MM/yyyy")
        self.data_dict[self.key] = date_str
        self.date_changed.emit(date)


class ImageWorker(QObject):
    image_loaded = Signal(QPixmap)  # Señal emitida cuando se carga la imagen

    def __init__(self, image_url: str) -> None:
        super().__init__()
        self.image_url = image_url

    def run(self) -> None:
        try:
            response = requests.get(self.image_url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data.read())
            self.image_loaded.emit(pixmap)
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")


class GraphicsViewController:
    def __init__(self, graphics_view: QGraphicsView, data_dict: dict, key: str) -> None:
        self.graphics_view = graphics_view
        self.data_dict = data_dict
        self.key = key
        self.scene = QGraphicsScene(self.graphics_view)
        self.graphics_view.setScene(self.scene)
        image_url = self.get_image_url(self.data_dict.get(self.key, ""))
        if not image_url:
            return
        self.show_loading_text()
        self.thread = QThread()
        self.worker = ImageWorker(image_url)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.image_loaded.connect(self.display_image)
        self.worker.image_loaded.connect(self.thread.quit)
        self.thread.start()

    def show_loading_text(self):
        # Mostrar "Cargando..." en el centro del QGraphicsView
        loading_text_item = QGraphicsTextItem("Cargando...")
        font = QFont("Arial", 16)
        loading_text_item.setFont(font)
        
        # Añadir el texto a la escena
        self.scene.addItem(loading_text_item)
        
        # Centrar el texto
        rect = self.graphics_view.viewport().rect()
        loading_text_item.setPos(rect.width() / 2 - loading_text_item.boundingRect().width() / 2,
                                 rect.height() / 2 - loading_text_item.boundingRect().height() / 2)

    def get_image_url(self, drive_url: str) -> str:
        if 'drive.google.com' in drive_url:
            try:
                file_id = drive_url.split('/d/')[1].split('/')[0]
                return f"https://drive.google.com/uc?export=download&id={file_id}"
            except IndexError:
                print(drive_url)
                print("[GRAPHICS_VIEW_CONTROLLER] Invalid Google Drive URL")
        return ""

    def load_image(self, image_url: str) -> None:
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            pixmap = QPixmap()
            if pixmap.loadFromData(image_data.read()):
                self.display_image(pixmap)
            else:
                print("Failed to load the image.")
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")

    @Slot(QPixmap)
    def display_image(self, pixmap: QPixmap) -> None:
        self.scene.clear()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(pixmap_item)
        self.graphics_view.fitInView(pixmap_item, Qt.KeepAspectRatioByExpanding)
        self.graphics_view.setAlignment(Qt.AlignCenter)
