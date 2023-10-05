from PyQt6 import QtCore, QtGui, QtWidgets
import des
import sys


# 创建解密窗口
class Ui_Forme(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Forme, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 436)
        Form.setWindowIcon(QtGui.QIcon('./img/b1.jpg'))

        # 设置密文显示文本框
        self.showc = QtWidgets.QTextBrowser(parent=Form)
        self.showc.setGeometry(QtCore.QRect(390, 155, 210, 110))
        self.showc.setObjectName("showc")

        # 设置加密按钮
        self.eButton = QtWidgets.QPushButton(parent=Form)
        self.eButton.setGeometry(QtCore.QRect(145, 283, 50, 45))
        self.eButton.setObjectName("eButton")
        self.eButton.clicked.connect(self.entry)

        # 设置按钮和输入框所在的frame
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setGeometry(QtCore.QRect(20, 320, 561, 121))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        # 创建labels和输入框
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(90, 40, 26, 16))
        self.label.setObjectName("label")
        self.key = QtWidgets.QLabel(parent=self.frame)
        self.key.setGeometry(QtCore.QRect(90, 80, 26, 16))
        self.key.setObjectName("key")
        self.pline = QtWidgets.QLineEdit(parent=self.frame)
        self.pline.setGeometry(QtCore.QRect(120, 40, 95, 20))
        self.pline.setObjectName("pline")
        self.kline = QtWidgets.QLineEdit(parent=self.frame)
        self.kline.setGeometry(QtCore.QRect(120, 80, 95, 20))
        self.kline.setObjectName("kline")

        # 设置窗口大标题
        self.title = QtWidgets.QLabel(parent=Form)
        self.title.setGeometry(QtCore.QRect(140, 10, 301, 101))
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
        self.en = QtWidgets.QLabel(parent=Form)
        self.en.setGeometry(QtCore.QRect(430, 80, 101, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 172))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 172))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        self.en.setPalette(palette)
        self.en.setObjectName("en")

        # 设置listview创建背景
        self.listView = QtWidgets.QListView(parent=Form)
        self.listView.setGeometry(QtCore.QRect(-10, -20, 641, 541))
        self.listView.setStyleSheet("background-image: url(./img/b1.jpg);")
        self.listView.setObjectName("listView")

        self.listView.raise_()
        self.showc.raise_()
        self.eButton.raise_()
        self.frame.raise_()
        self.title.raise_()
        self.en.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "加密"))
        self.eButton.setWhatsThis(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:18pt; color:#55ffff;\">""加密</span></p></body></html>"))
        self.eButton.setText(_translate("Form", "加密"))
        self.label.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:9.5pt; font-weight:700;\">明文</span></p></body></html>"))
        self.key.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:9.5pt; font-weight:700;\">密钥</span></p></body></html>"))
        self.title.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:72pt; font-weight:700;\">S-DES</span></p></body></html>"))
        self.en.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:28pt; font-weight:700;\">加密</span></p></body></html>"))

    # 定义加密函数
    def entry(self):
        plain = self.pline.text()
        key = self.kline.text()
        if key == "":
            self.showc.setText("请输入正确的十位二进制数作为密钥！")
        else:
            if des.is_bin_string(plain) is True:
                plain = plain.zfill(8)
            self.showc.setText("密文为：")
            self.showc.append(str(des.C(plain, key)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_Forme()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
