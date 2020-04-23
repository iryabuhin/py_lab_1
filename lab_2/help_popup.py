from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

class Ui_help_popup(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_help_popup, self).__init__()
        self.setFixedHeight(200)
        self.setFixedWidth(200)

    def setupUi(self, help_popup):
        self.label = QtWidgets.QTextBrowser(help_popup)
        self.label.setGeometry(QtCore.QRect(10, 10, 450, 200))
        self.label.setObjectName("label")
        self.close_button = QtWidgets.QPushButton(help_popup)
        self.close_button.setGeometry(QtCore.QRect(175, 215, 100, 25))
        self.close_button.setText('OK')
        self.close_button.clicked.connect(help_popup.close)


        self.retranslateUi(help_popup)
        QtCore.QMetaObject.connectSlotsByName(help_popup)

    def retranslateUi(self, help_popup):
        _translate = QtCore.QCoreApplication.translate
        help_popup.setWindowTitle(_translate("help_popup", "Help"))
        # self.label.setText(_translate("help_popup", "LoremIpsum"))

    def set_help_message(self, path):
        pass



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    help_popup = QtWidgets.QWidget()
    ui = Ui_help_popup()
    ui.setupUi()
    help_popup.show()
    sys.exit(app.exec_())
