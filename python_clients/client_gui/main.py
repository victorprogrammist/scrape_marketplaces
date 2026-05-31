
import sys
import asyncio
import client_tools.api
import tools.ozy_tools

from PySide6.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton,
    QCheckBox, QComboBox,
    QProgressBar,
    QGroupBox, QTabWidget, QTextEdit)

from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIntValidator, QDoubleValidator

from qasync import QEventLoop, asyncSlot

class MyWindow(QWidget):


    def make_parameters(self):

        def as_float(s):
            if not s:
                return 0
            if s.find('.') < 0 and s.find(',') < 0:
                return int(s)
            return float(s)

        res = {}

        res['search_string'] = self.e_search_string.text()
        res['url_category'] = self.e_url_category.text()
        res['expected_count_items'] = as_float(self.e_expected_count_items.text())
        res['min_price'] = as_float(self.e_min_price.text())
        res['max_price'] = as_float(self.e_max_price.text())
        res['sorting'] = self.combo_sorting.currentText()
        res['format_as_csv'] = self.checkbox_csv.isChecked()

        return res


    async def make_request(self):

        query = self.make_parameters()
        try:
            return await client_tools.api.make_request(query)
        except Exception as e:
            return tools.ozy_tools.format_error(e)


    def append_result(self, msg):

        num = self.result_count + 1
        self.result_count = num

        result_text_edit = QTextEdit()
        result_text_edit.setReadOnly(True)
        result_text_edit.setText(msg)

        tab_result = QWidget()
        self.tab_widget.addTab(tab_result, f"Результат {num}")

        result_layout = QVBoxLayout(tab_result)
        result_layout.addLayout(self.make_result_buttons(result_text_edit, tab_result))
        result_layout.addWidget(result_text_edit)

        self.tab_widget.setCurrentWidget(tab_result)


    def make_result_buttons(self, result_text_edit, result_widget):

        bt_copy = QPushButton("Копировать в буфер")
        bt_save = QPushButton("Записать в файл")
        bt_close = QPushButton("Закрыть результат")

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addSpacing(10)
        hbox_buttons.addWidget(bt_copy)
        hbox_buttons.addSpacing(10)
        hbox_buttons.addWidget(bt_save)
        hbox_buttons.addSpacing(10)
        hbox_buttons.addWidget(bt_close)
        hbox_buttons.addStretch(1)

        bt_copy.clicked.connect(lambda: self.copy_to_clipboard(result_text_edit))
        bt_save.clicked.connect(lambda: self.save_to_file(result_text_edit))
        bt_close.clicked.connect(lambda: self.close_result(result_widget))

        return hbox_buttons


    def close_result(self, result_widget):
        index = self.tab_widget.indexOf(result_widget)
        if index >= 0:
            self.tab_widget.removeTab(index)  # Удаляем с экрана
            result_widget.deleteLater()

    def copy_to_clipboard(self, result_text_edit):
        text = result_text_edit.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)


    def save_to_file(self, result_text_edit):

        text = result_text_edit.toPlainText().strip()
        if not text:
            return

        from PySide6.QtWidgets import QFileDialog

        if text[0] in '[{' and text[-1] in '}]':
            ext = 'JSON Files (*.json)'
        else:
            ext = 'CSV Files (*.csv)'

        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Сохранить результат",
            "",
            f"{ext};;Text Files (*.txt);;All Files (*)",
            options=QFileDialog.Option.DontUseNativeDialog
        )

        if not file_path:
            return

        ext = ""
        if "*." in selected_filter:
            ext = selected_filter.split("*.")[1].replace(")", "")

        if ext and ext != "*" and not file_path.lower().endswith(f".{ext}"):
            file_path = f"{file_path}.{ext}"

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)

        except Exception as e:
            self.make_message('Ошибка', "Ошибка сохранения", str(e))


    def make_message(self, caption, text, text_extended):

        from PySide6.QtWidgets import QMessageBox

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(caption)

        if text:
            msg.setText(text)

        if text_extended:
            msg.setInformativeText(text_extended)

        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg.exec()

    def escEvent(self):
        if 0 == self.tab_widget.currentIndex():
            self.close()
            return

        self.close_result(self.tab_widget.currentWidget())


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.escEvent()
        else:
            super().keyPressEvent(event)


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Скрапинг МаркетПлейсов")
        self.resize(500, 300)

        self.tab_widget = QTabWidget()
        tab_filters = QWidget()
        self.tab_widget.addTab(tab_filters, "Условия отбора")

        self.result_count = 0

        #*************************************************************
        filters_layout = QVBoxLayout(tab_filters)
        filters_layout.addWidget(self.make_inputs())
        filters_layout.addLayout(self.make_buttons())
        filters_layout.addWidget(self.make_progress_bar())
        filters_layout.addStretch(1)

        #******************************************************************
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)
        #*********************************

        self.load_settings()


    def make_input(self, form_layout, name, caption):

        line = QLineEdit()
        setattr(self, name, line)
        form_layout.addRow(caption, line)

        return line


    def make_inputs(self):

        form_layout = QFormLayout()

        #************************
        self.make_input(form_layout, 'e_search_string', "Строка поиска")

        self.make_input(form_layout, 'e_url_category', "Урл категории")

        line = self.make_input(form_layout, 'e_expected_count_items', "Количество")
        line.setValidator(QIntValidator(0, 999999, self))

        price_validator = QDoubleValidator(0.0, 999999.99, 2, self)
        price_validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        line = self.make_input(form_layout, 'e_min_price', "Минимальная цена")
        line.setValidator(price_validator)

        line = self.make_input(form_layout, 'e_max_price', "Максимальная цена")
        line.setValidator(price_validator)

        #************************
        self.combo_sorting = QComboBox()

        self.combo_sorting.addItems([
            "Популярные",
            "Новинки",
            "Дешевле",
            "Дороже",
            "С высоким рейтингом",
            "С большими скидками"
            ])

        form_layout.addRow('Сортировка', self.combo_sorting)

        #************************
        self.checkbox_csv = QCheckBox("Получить как CSV")
        form_layout.addRow('', self.checkbox_csv)
        #************************

        self.form_group = QGroupBox()
        self.form_group.setLayout(form_layout)

        return self.form_group


    def make_progress_bar(self):

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)  # Скрываем текст "0%"
        self.progress_bar.setVisible(False)      # Изначально делаем его невидимым
        self.progress_bar.setRange(0, 0)

        return self.progress_bar


    def make_buttons(self):

        self.button_ok = QPushButton("Получить")
        self.button_cancel = QPushButton("Закрыть")
        self.button_default = QPushButton("Очистить условия")

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addSpacing(40)
        hbox_buttons.addWidget(self.button_ok)
        hbox_buttons.addWidget(self.button_cancel)
        hbox_buttons.addSpacing(40)
        hbox_buttons.addWidget(self.button_default)
        hbox_buttons.addStretch(1)

        self.button_ok.clicked.connect(self.on_ok_clicked)
        self.button_default.clicked.connect(self.clear_settings)
        self.button_cancel.clicked.connect(self.close)

        return hbox_buttons


    @asyncSlot()
    async def on_ok_clicked(self):

        def set_enabled(f):
            self.form_group.setEnabled(f)
            self.button_ok.setEnabled(f)
            self.button_default.setEnabled(f)
            self.progress_bar.setVisible(not f)

        set_enabled(False)
        res = await self.make_request()
        self.append_result(res)
        set_enabled(True)


    def closeEvent(self, event):
        self.save_settings()
        event.accept()


    def clear_settings(self):
        self.settings.clear()
        self.load_settings()


    def load_settings(self):

        if not hasattr(self, 'settings'):
            self.settings = QSettings("Ozy", "Gui")

        self.e_search_string.setText(
            self.settings.value("e_search_string", "вкусняшка"))

        self.e_url_category.setText(
            self.settings.value("e_url_category", ""))

        self.e_expected_count_items.setText(
            self.settings.value("e_expected_count_items", "100"))

        self.e_min_price.setText(self.settings.value("e_min_price", ""))
        self.e_max_price.setText(self.settings.value("e_max_price", ""))

        self.checkbox_csv.setChecked(
            self.settings.value("checkbox_csv", False, type=bool))

        self.combo_sorting.setCurrentIndex(
            self.settings.value("combo_sorting", 0, type=int))


    def save_settings(self):

        self.settings.setValue("e_search_string", self.e_search_string.text())
        self.settings.setValue("e_url_category", self.e_url_category.text())

        self.settings.setValue("e_expected_count_items", self.e_expected_count_items.text())
        self.settings.setValue("e_min_price", self.e_min_price.text())
        self.settings.setValue("e_max_price", self.e_max_price.text())

        self.settings.setValue("checkbox_csv", self.checkbox_csv.isChecked())

        self.settings.setValue("combo_sorting", self.combo_sorting.currentIndex())



def main():

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MyWindow()
    window.show()

    with loop:
        loop.run_forever()

    return 0

