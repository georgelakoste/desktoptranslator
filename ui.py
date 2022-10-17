from PyQt5 import QtWidgets, QtCore
from googletrans import Translator
import codecs


class TranslatorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.setFixedSize(QtCore.QSize(1600, 900))
        self.setStyleSheet('background-color:white;')
        self.setWindowTitle('Переводчик')

        self.translator = Translator()
        self.langs = ['ru', 'en', 'fr', 'it', 'de']
        self.active_input_lang = 'ru'
        self.active_output_lang = 'en'
        self.langsToUI = {'ru': 'Русский', 'en': 'Английский', 'fr': 'Французский', 'it': 'Итальянский',
                          'de': 'Немецкий'}
        self.max_char = 15000

        self.not_active_button_css = 'background-color:white;'
        self.active_button_css = 'background-color:white; color:blue'
        self.input_text = QtWidgets.QTextEdit(parent=self.centralWidget())
        self.input_text.textChanged.connect(self.update_counter)
        self.input_text.setFixedSize(QtCore.QSize(750, 550))
        self.input_text.move(38, 225)
        self.input_lang_chooser_w = QtWidgets.QWidget(parent=self.centralWidget())
        self.input_lang_chooser = self.generate_languages_layout(self.setActiveInputLang)
        self.input_lang_chooser_w.setLayout(self.input_lang_chooser)
        self.input_lang_chooser_w.move(213, 150)

        self.output_text = QtWidgets.QTextEdit(parent=self.centralWidget())
        self.output_text.setReadOnly(True)
        self.output_text.setFixedSize(QtCore.QSize(750, 550))
        self.output_text.move(812, 225)
        self.output_lang_chooser_w = QtWidgets.QWidget(parent=self.centralWidget())
        self.output_lang_chooser = self.generate_languages_layout(self.setActiveOutputLang)
        self.output_lang_chooser_w.setLayout(self.output_lang_chooser)
        self.output_lang_chooser_w.move(913, 150)
        self.activate_languages()

        self.translate_button = QtWidgets.QPushButton(parent=self.centralWidget())
        self.translate_button.setText('Перевести')
        self.translate_button.clicked.connect(lambda: self.output_text.setText(self.translate()))
        self.translate_button.move(740, 800)

        self.symbol_counter = QtWidgets.QLabel(parent=self.centralWidget())
        self.symbol_counter.move(650, 750)
        self.symbol_counter.setText('15000 / 15000')
        self.symbol_counter.setFixedWidth(self.symbol_counter.width())
        self.update_counter()

        self.import_button = QtWidgets.QPushButton(parent=self.centralWidget())
        self.import_button.setText('Импортировать из файла')
        self.import_button.clicked.connect(self.import_and_paste)
        self.import_button.move(38, 50)

        self.export_button = QtWidgets.QPushButton(parent=self.centralWidget())
        self.export_button.setText('Экспортировать в файл')
        self.export_button.clicked.connect(self.export_to)
        self.export_button.move(812, 50)

    def generate_languages_layout(self, connectfunc):
        layout = QtWidgets.QHBoxLayout()
        for lang in self.langs:
            lang_button = QtWidgets.QPushButton()
            lang_button.setObjectName(lang)
            lang_button.setText(self.langsToUI[lang])
            lang_button.clicked.connect(lambda: connectfunc(self.sender().objectName()))
            layout.addWidget(lang_button)
            del lang_button
        return layout

    def setActiveInputLang(self, lang):
        if lang != self.active_output_lang:
            self.active_input_lang = lang
        else:
            self.active_input_lang, self.active_output_lang = self.active_output_lang, self.active_input_lang
            i = self.input_text.toPlainText()
            self.input_text.setText(self.output_text.toPlainText())
            self.output_text.setText(i)
        self.activate_languages()

    def setActiveOutputLang(self, lang):
        if lang != self.active_input_lang:
            self.active_output_lang = lang
        else:
            self.active_input_lang, self.active_output_lang = self.active_output_lang, self.active_input_lang
            i = self.input_text.toPlainText()
            self.input_text.setText(self.output_text.toPlainText())
            self.output_text.setText(i)
        self.activate_languages()

    def translate(self):
        if self.input_text.toPlainText() == '':
            dialog = QtWidgets.QMessageBox()
            dialog.critical(self, 'Ошибка!', 'В поле ввода текста пусто')
            return
        string = []
        if len(self.input_text.toPlainText()) > 5000:
            str_count = 0
            while str_count < len(self.input_text.toPlainText()):
                right = str_count + 5000 if str_count + 5000 < len(self.input_text.toPlainText()) else len(
                    self.input_text.toPlainText()) - 1
                string.append(self.input_text.toPlainText()[str_count:right])
                str_count += 5000
        else:
            string = [self.input_text.toPlainText()]
        new_text = ''
        for i in string:
            new_text += self.translator.translate(i, dest=self.active_output_lang, src=self.active_input_lang).text
        return new_text

    def activate_languages(self):
        for i in range(len(self.langs)):
            if self.input_lang_chooser.itemAt(i).widget().objectName() == self.active_input_lang:
                self.input_lang_chooser.itemAt(i).widget().setStyleSheet(self.active_button_css)
            else:
                self.input_lang_chooser.itemAt(i).widget().setStyleSheet(self.not_active_button_css)
            if self.output_lang_chooser.itemAt(i).widget().objectName() == self.active_output_lang:
                self.output_lang_chooser.itemAt(i).widget().setStyleSheet(self.active_button_css)
            else:
                self.output_lang_chooser.itemAt(i).widget().setStyleSheet(self.not_active_button_css)

    def update_counter(self):
        if len(self.input_text.toPlainText()) > self.max_char:
            self.input_text.setText(self.input_text.toPlainText()[0:self.max_char])
        ns = f"{len(self.input_text.toPlainText())} / 15000"
        self.symbol_counter.setText(ns)

    def import_and_paste(self):
        dialog = QtWidgets.QFileDialog()
        path = dialog.getOpenFileNames(self, 'Выберите файл', filter='Текстовые файлы (*.txt)')
        if path[0] == [] or path[1] == '':
            return
        else:
            text = codecs.open(path[0][0], 'r', 'utf-8').readlines()
            for i in text:
                self.input_text.setText(self.input_text.toPlainText() + i)

    def export_to(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить файл как", "",
                                                     "Text documents (*.txt)")
        if path[0] == 0 or path[1] == '':
            return
        file = open(path[0], 'w')
        file.write(self.output_text.toPlainText())
