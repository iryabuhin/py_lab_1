from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QTextBrowser, \
    QWidget, QPushButton, QSpinBox, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSlot
from help_popup import Ui_help_popup
import quadr_eq
import lin_eq_system
import numpy as np
import sys


class UiMainWindow(QMainWindow):
    mode: int
    equations: list = []

    def __init__(self):
        super(UiMainWindow, self).__init__()
        self.mode = 1
        self.equations = []
        self.setup_ui(MainWindow)

    def setup_ui(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 520)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setHorizontalSpacing(2)
        self.grid.setVerticalSpacing(5)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')

        self.label = QLabel(self.centralwidget)
        self.label.setFont(self.centralwidget.font())
        self.label.setObjectName('label')
        self.grid.addWidget(self.label, 0, 0, 1, 1)
        self.label.setFixedHeight(20)

        self.method_choice = QtWidgets.QComboBox(self.centralwidget)
        self.method_choice.setFont(self.centralwidget.font())
        self.method_choice.addItem('Crammers')
        self.method_choice.addItem('Gaussian Elimination')
        self.method_choice.addItem('Matrix method')
        self.method_choice.setFixedHeight(25)
        self.method_choice.hide()

        self.add_equation_btn = QPushButton(self.centralwidget)
        self.add_equation_btn.setText('Добавить ур-е к системе')
        self.add_equation_btn.setFont(self.centralwidget.font())
        self.add_equation_btn.clicked.connect(self.append_equation)
        self.add_equation_btn.setFixedHeight(25)
        self.add_equation_btn.hide()

        self.grid.addWidget(self.method_choice, 7, 0, 1, 2)
        self.grid.addWidget(self.add_equation_btn, 7, 2, 1, 2)

        self.mode_selection_box = QtWidgets.QComboBox(self.centralwidget)
        self.mode_selection_box.currentIndexChanged.connect(self.change_mode)
        self.grid.addWidget(self.mode_selection_box, 1, 0, 1, 4)

        self.mode_selection_box.setFont(self.centralwidget.font())
        self.mode_selection_box.setObjectName('mode_selection_box')
        self.mode_selection_box.addItem('')
        self.mode_selection_box.addItem('')

        self.help_button = QPushButton(self.centralwidget)
        self.help_button.setFont(self.centralwidget.font())
        self.help_button.clicked.connect(self.on_help_btn_clicked)
        self.grid.addWidget(self.help_button, 1, 4, 1, 1)

        self.output_text_field = QTextBrowser(self.centralwidget)
        self.output_text_field.setObjectName('output_text_field')
        self.grid.addWidget(self.output_text_field, 2, 0, 4, 5)

        self.input_field = QLineEdit(self.centralwidget)
        self.input_field.setObjectName("textInput")
        self.grid.addWidget(self.input_field, 5, 0, 1, 5)

        self.clear_btn = QPushButton(self.centralwidget)
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.clicked.connect(self.output_text_field.clear)

        self.clear_btn.setFont(self.centralwidget.font())
        self.grid.addWidget(self.clear_btn, 6, 0, 1, 1)

        self.submit_button = QPushButton(self.centralwidget)
        self.submit_button.clicked.connect(self.process)
        self.grid.addWidget(self.submit_button, 6, 4, 1, 1)

        self.submit_button.setFont(self.centralwidget.font())
        self.submit_button.setObjectName('submitButton')

        self.font_selection_box = QtWidgets.QFontComboBox(self.centralwidget)
        self.font_selection_box.setObjectName("fontSelectionBox")
        self.font_selection_box.setFont(self.centralwidget.font())
        self.grid.addWidget(self.font_selection_box, 6, 2, 1, 1)

        self.font_size_spin_box = QSpinBox(self.centralwidget)
        self.font_size_spin_box.setObjectName("fontSizeSpinBox")
        self.font_size_spin_box.setValue(11)
        self.font_size_spin_box.setSingleStep(1)
        self.font_size_spin_box.setRange(5, 22)
        self.font_size_spin_box.valueChanged.connect(self.change_output_box_font_value)
        self.font_selection_box.activated.connect(self.change_output_box_font_family)
        self.grid.addWidget(self.font_size_spin_box, 6, 3, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.font_size_spin_box.setFixedHeight(25)
        self.font_selection_box.setFixedHeight(25)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)

        MainWindow.setStatusBar(self.statusbar)
        self.save_output = QtWidgets.QAction(MainWindow)
        self.save_output.triggered.connect(self.save_output_to_file)
        self.save_output.setShortcut('Ctrl+S')

        self.close_button = QtWidgets.QAction(MainWindow)
        self.close_button.triggered.connect(MainWindow.close)
        self.close_button.setShortcut('Ctrl+X')

        self.menuFile.addAction(self.save_output)
        self.menuFile.addAction(self.close_button)
        self.menubar.addAction(self.menuFile.menuAction())

        self.centralwidget.setLayout(self.grid)

        self.translate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def translate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Лабораторная работа 2"))
        self.submit_button.setText(_translate("MainWindow", "Решить"))
        self.clear_btn.setText(_translate("MainWindow", "Очистить"))
        self.label.setText(_translate("MainWindow", "Выберите режим:"))

        self.mode_selection_box.setItemText(0, _translate("MainWindow", "Квадратное уравнение"))
        self.mode_selection_box.setItemText(1, _translate("MainWindow", "СЛАУ"))
        self.help_button.setText(_translate("MainWindow", "Помощь"))

        self.menuFile.setTitle(_translate("MainWindow", "Файл"))

        self.save_output.setText(_translate("MainWindow", "Сохранить"))
        self.save_output.setStatusTip(_translate("MainWindow", "Сохранить весь вывод текстового поля в файл"))

        self.close_button.setText(_translate("MainWindow", "Закрыть"))
        self.close_button.setStatusTip(_translate("MainWindow", "Закрыть приложение"))

    @pyqtSlot()
    def save_output_to_file(self):
        text = self.output_text_field.toPlainText()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл', 'output.data', 'Все файлы (*)', options=options)
        with open(filename, 'w') as f:
            f.write(text)


    @pyqtSlot()
    def change_output_box_font_value(self):
        font = self.font_selection_box.currentFont()
        font.setPointSize(self.font_size_spin_box.value())
        self.output_text_field.setFont(font)
        self.centralwidget.setFont(font)

    @pyqtSlot()
    def change_output_box_font_family(self):
        font = self.font_selection_box.currentFont()
        self.output_text_field.setFont(font)
        self.centralwidget.setFont(font)

    def change_mode(self):
        if self.mode == 1:
            self.mode = 2
            self.add_equation_btn.show()
            self.method_choice.show()

        elif self.mode == 2:
            self.mode = 1
            self.add_equation_btn.hide()
            self.method_choice.hide()
            self.equations.clear()

    @pyqtSlot()
    def process(self):
        expr = self.input_field.text()
        try:
            if self.mode == 1:
                self.output_text_field.insertPlainText(expr + '\n')
                self.solve_quadr_eq(expr)
                self.input_field.clear()
            else:
                self.solve_linear_system()
                self.equations.clear()
        except Exception as err:
            self.show_popup(text='Возникло исключение', title='Ошибка',
                            detailed_text=str(err))
            self.input_field.clear()
            self.output_text_field.clear()
            self.equations.clear()


    @pyqtSlot()
    def solve_quadr_eq(self, expr):
        if not expr:
            self.show_popup(
                text='Введите уравнение!',
                title='Пустой ввод',
                icon=QMessageBox.Information
            )
            return

        coeffs = quadr_eq.parse_equation(expr)
        a = b = c = 0
        a, b, c = coeffs

        roots = np.roots([a, b, c]).tolist()
        roots = [round(x, 2) for x in roots] if not isinstance(roots[0], complex) else roots

        self.output_text_field.insertPlainText('Решение квадратного ур-я:\n\t')
        if isinstance(roots[0], complex):
            self.output_text_field.insertPlainText(('Комплексные корни:\n\t'))
            for x in roots:
                self.output_text_field.insertPlainText(f'{str(x)}\n\t')
            return

        self.output_text_field.insertPlainText('\t'.join([str(x) for x in roots]) + '\n')
        self.output_text_field.insertPlainText('\nПроверка подстановкой:\n')
        x1, x2 = roots
        self.output_text_field.insertPlainText(f"a*x1^2 + b*x1 + c = {eval('a * x1**2 + b*x1 + c')}\n")
        self.output_text_field.insertPlainText(f"a*^2 + b*x2 + c = {eval('a * x2**2 + b*x2 + c')}\n")

    @pyqtSlot()
    def append_equation(self):
        if self.mode == 2:
            if self.input_field.text():
                self.equations.append(self.input_field.text().rstrip())
                self.output_text_field.insertPlainText(self.input_field.text() + '\n')
                self.input_field.clear()
            else:
                self.show_popup(
                    text='Введите уравнение!',
                    title='Пустой ввод',
                    icon=QMessageBox.Information
                )

    @pyqtSlot()
    def solve_linear_system(self):
        matrix = [lin_eq_system.parse_equation(l) for l in self.equations if l != '']
        A = []
        for row in matrix:
            A.append(row[:-1])

        B = [row[-1] for row in matrix]

        self.output_text_field.insertPlainText('Матрица коэфф. уравнений и вектор свободных коэфф.:\n')
        for i in range(len(A)):
            self.output_text_field.insertPlainText('| {} |'.format('\t'.join([str(x) for x in A[i]])))
            self.output_text_field.insertPlainText(' ')
            self.output_text_field.insertPlainText('| {} |\n'.format(str(B[i])))

        solution = []
        if self.method_choice.currentIndex() == 0:
            solution = lin_eq_system.crammers_rule(A, B)
        elif self.method_choice.currentIndex() == 1:
            solution = lin_eq_system.gaussian_elimination(A, B)
        elif self.method_choice.currentIndex() == 2:
            solution = lin_eq_system.matrix_method(A, B)

        self.output_text_field.insertPlainText('Решение системы:\n\t')
        self.output_text_field.insertPlainText('\t'.join([str(x) for x in solution]))


    def show_popup(self, text: str, icon=QMessageBox.Critical,
                   title='', inf_text='', detailed_text=''):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)

        if inf_text:
            msg.setInformativeText(inf_text)

        if detailed_text:
            msg.setDetailedText(detailed_text)

        x = msg.exec_()

    @pyqtSlot()
    def on_help_btn_clicked(self):
        self.help_popup = QtWidgets.QWidget()
        self.ui = Ui_help_popup()
        self.ui.setupUi(self.help_popup)
        self.ui.retranslateUi(self.help_popup)
        help_msg = ''
        if self.mode == 1:
            help_msg += '''
    Решает введённое квадратное уравнение.
    Формат ввода:
    ax^2 +-bx +-c = +-c
    '''
        else:
            help_msg += '''
    Решает систему линейных уравнений при нажатии кнопки "Решить".
    Добавить уравнение к системе можно введя его в поле ввода и нажав кнопку "Добавить уравнение к системе".
    '''
        help_msg += '\nCtrl+S - сохранить весь вывод в окне программы в файл'
        help_msg += '\nCtrl+X - выход из программы'
        self.ui.label.setText(help_msg)
        self.help_popup.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
