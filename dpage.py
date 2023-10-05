from PyQt6 import QtCore, QtGui, QtWidgets
import des
import sys


class Ui_Formd(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Formd, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 436)
        Form.setWindowIcon(QtGui.QIcon('./img/b2.jpg'))
        
        # 设置明文显示文本框
        self.showp = QtWidgets.QTextBrowser(parent=Form)
        self.showp.setGeometry(QtCore.QRect(410, 323, 120, 50))
        self.showp.setObjectName("showp")

        # 设置解密按钮
        self.dButton = QtWidgets.QPushButton(parent=Form)
        self.dButton.setGeometry(QtCore.QRect(155, 155, 35, 30))
        self.dButton.setObjectName("dButton")
        self.dButton.clicked.connect(self.decipher)

        # 设置按钮和输入框所在的frame
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setGeometry(QtCore.QRect(-55, 280, 251, 131))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        # 创建labels和输入框
        self.ciphertext = QtWidgets.QLabel(parent=self.frame)
        self.ciphertext.setGeometry(QtCore.QRect(90, 40, 24, 16))
        self.ciphertext.setObjectName("ciphertext")
        self.key = QtWidgets.QLabel(parent=self.frame)
        self.key.setGeometry(QtCore.QRect(90, 80, 24, 16))
        self.key.setObjectName("key")
        self.cline = QtWidgets.QLineEdit(parent=self.frame)
        self.cline.setGeometry(QtCore.QRect(120, 40, 132, 20))
        self.cline.setObjectName("cline")
        self.kline = QtWidgets.QLineEdit(parent=self.frame)
        self.kline.setGeometry(QtCore.QRect(120, 80, 132, 20))
        self.kline.setObjectName("kline")

        # 设置窗口大标题
        self.title = QtWidgets.QLabel(parent=Form)
        self.title.setGeometry(QtCore.QRect(55, 10, 301, 101))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 0, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        self.title.setPalette(palette)
        self.title.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.title.setScaledContents(False)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")

        # 设置窗口小标题
        self.de = QtWidgets.QLabel(parent=Form)
        self.de.setGeometry(QtCore.QRect(470, 50, 101, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 172))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 172))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        self.de.setPalette(palette)
        self.de.setObjectName("de")

        # 设置listview创建背景
        self.listView = QtWidgets.QListView(parent=Form)
        self.listView.setGeometry(QtCore.QRect(-10, -20, 641, 541))
        self.listView.setStyleSheet("background-image: url(./img/b2.jpg);")
        self.listView.setObjectName("listView")
        
        self.listView.raise_()
        self.showp.raise_()
        self.dButton.raise_()
        self.frame.raise_()
        self.title.raise_()
        self.de.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        # 设置显示的内容
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "解密"))
        self.dButton.setWhatsThis(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:18pt; color:#55ffff;\">加密</span></p></body></html>"))
        self.dButton.setText(_translate("Form", "解密"))
        self.ciphertext.setText(_translate("Form", "密文"))
        self.key.setText(_translate("Form", "密钥"))
        self.title.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:72pt; font-weight:700;\">S-DES</span></p></body></html>"))
        self.de.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:28pt; font-weight:700;\">解密</span></p></body></html>"))

    def decipher(self):
        # 定义解密函数
        cy = self.cline.text()
        key = self.kline.text()
        if key == "":
            self.showp.setText("请输入正确的十位二进制数作为密钥！")
        else:
            self.showp.setText("明文为：")
            self.showp.append(str(des.P(cy, key)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_Formd()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
    
