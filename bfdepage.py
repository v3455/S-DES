from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QInputDialog
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import numpy as np
import time
import des
import sys


class NewThread(threading.Thread):
    # 定义多线程类
    key = 0
    threads = []
    result_list = []
    lock = threading.Lock()
    stime = []
    etime = []
    r_time = []

    def task(self, num, plain, cipher):
        # 实现多线程执行暴力破解与耗时的动图
        plain = plain.split(",")
        cipher = cipher.split(",")
        for i in range(num):
            # 每组明密文对开始一个线程
            thread = threading.Thread(target=self.get, args=(str(plain[i]), str(cipher[i])))
            self.stime.append(time.time())
            thread.start()
            self.threads.append(thread)
        for thread in self.threads:
            thread.join()
            self.etime.append(time.time())
        for j in range(num):
            # 计算每个线程耗时
            self.r_time.append(self.etime[j] - self.stime[j])
        self.key = set(self.result_list[0])
        for lst in self.result_list[1:]:
            # 计算交集获得共同密钥
            self.key.intersection_update(lst)

        fig, ax = plt.subplots()
        x = np.arange(len(self.r_time))
        # 初始画布
        bar = plt.bar(x, self.r_time)
        plt.xlabel("Thread ID")
        plt.ylabel("Runtime(s)")
        plt.title("Thread Runtime")
        ax.set_xticks(x)
        ax.set_xticklabels([f"Thread-{i + 1}" for i in range(len(self.r_time))])

        # 更新画面函数
        def animate(i):
            # 更新每个柱子的高度
            for rect, h in zip(bar, self.r_time):
                rect.set_height(h)
            return bar
        # 创建动画
        anim = FuncAnimation(fig, animate, frames=range(100), interval=200, blit=True)
        # 保存动图
        anim.save('time.gif', dpi=80, writer='Pillow')

    def get(self, plain, cipher):
        # 实现暴力破解
        lst = des.brute_force_decrypt(plain, cipher)
        self.lock.acquire()
        # 加锁
        try:
            # 将每个线程写出的列表添加到result_list中
            self.result_list.append(lst)
        finally:
            # 释放锁
            self.lock.release()


class Ui_Formbf(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Formbf, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 436)
        Form.setWindowIcon(QtGui.QIcon('./img/b3.jpg'))
        
        # 设置密钥显示文本框
        self.showk = QtWidgets.QTextBrowser(parent=Form)
        self.showk.setGeometry(QtCore.QRect(540, 250, 90, 95))
        self.showk.setObjectName("textBrowser")

        # 设置暴力破解按钮和多线程破解按钮
        self.pButton = QtWidgets.QPushButton(parent=Form)
        self.pButton.setGeometry(QtCore.QRect(200, 175, 31, 31))
        self.pButton.setObjectName("pButton")
        self.pButton.clicked.connect(self.decry)
        self.tButton = QtWidgets.QPushButton(parent=Form)
        self.tButton.setGeometry(QtCore.QRect(500, 175, 81, 31))
        self.tButton.setObjectName("tButton")
        self.tButton.clicked.connect(self.showDialog)

        # 设置按钮和输入框所在的frame
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setGeometry(QtCore.QRect(-1, 220, 261, 131))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        # 创建labels和输入框
        self.pline = QtWidgets.QLineEdit(parent=self.frame)
        self.pline.setGeometry(QtCore.QRect(120, 50, 132, 20))
        self.pline.setObjectName("pline")
        self.cline = QtWidgets.QLineEdit(parent=self.frame)
        self.cline.setGeometry(QtCore.QRect(120, 80, 132, 20))
        self.cline.setObjectName("cline")
        self.plain = QtWidgets.QLabel(parent=self.frame)
        self.plain.setGeometry(QtCore.QRect(82, 50, 40, 20))
        self.cipher = QtWidgets.QLabel(parent=self.frame)
        self.cipher.setGeometry(QtCore.QRect(82, 80, 40, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(28, 75, 219))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        self.plain.setPalette(palette)
        self.cipher.setPalette(palette)
        self.plain.setObjectName("plain")
        self.cipher.setObjectName("cipher")

        # 设置窗口大标题
        self.title = QtWidgets.QLabel(parent=Form)
        self.title.setGeometry(QtCore.QRect(80, 10, 301, 101))
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
        self.task = QtWidgets.QLabel(parent=Form)
        self.task.setGeometry(QtCore.QRect(475, 50, 163, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 172))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 172))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        self.task.setPalette(palette)
        self.task.setObjectName("task")
        
        # 设置listview创建背景
        self.listView = QtWidgets.QListView(parent=Form)
        self.listView.setGeometry(QtCore.QRect(-10, -60, 641, 541))
        self.listView.setStyleSheet("background-image: url(./img/b3.jpg);")
        self.listView.setObjectName("listView")
        
        self.listView.raise_()
        self.showk.raise_()
        self.pButton.raise_()
        self.tButton.raise_()
        self.frame.raise_()
        self.title.raise_()
        self.task.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        # 设置显示的内容
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "暴力破解"))
        self.pButton.setWhatsThis(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:18pt; color:#55ffff;\">加密</span></p></body></html>"))
        self.pButton.setText(_translate("Form", "破解"))
        self.tButton.setWhatsThis(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:18pt; color:#55ffff;\">加密</span></p></body></html>"))
        self.tButton.setText(_translate("Form", "多线程破解"))
        self.plain.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:11pt; font-weight:700;\">明文</span></p></body></html>"))
        self.cipher.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\""
            "<span style=\" font-size:11pt; font-weight:700;\">密文</span></p></body></html>"))
        self.title.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:72pt; font-weight:700;\">S-DES</span></p></body></html>"))
        self.task.setText(_translate(
            "Form", "<html><head/><body><p align=\"center\">"
            "<span style=\" font-size:22pt; font-weight:700;\">暴力破解</span></p></body></html>"))

    def decry(self):
        # 单个明密文对的暴力破解
        cy = self.cline.text()
        plain = self.pline.text()
        key = des.brute_force_decrypt(plain, cy)
        self.showk.setText("密钥为：")
        for akey in key:
            if type(akey) == int:
                akey = bin(akey)[2:].zfill(10)
            self.showk.append(str(akey))

    def showDialog(self):
        # 通过输入对话框实现多个明密文对的读取与暴力破解
        num, okPressed = QInputDialog.getText(self, "第一步", "明密文对数量")
        if okPressed:
            plain, okPressed = QInputDialog.getText(self, "明密文对", "明文")
            if okPressed:
                cipher, okPressed = QInputDialog.getText(self, "明密文对", "密文")
                if okPressed:
                    num = int(num)
                    mythread = NewThread()
                    # 创建多线程实例
                    mythread.task(num, plain, cipher)
                    # 使用多线程实例进行暴力破解
                    self.showk.setText("密钥为：")
                    for akey in mythread.key:
                        if type(akey) == int:
                            akey = bin(akey)[2:].zfill(10)
                        self.showk.append(str(akey))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_Formbf()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
    
