from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import dpage
import epage
import bfdepage

# 定义主页界面
class Ui_MainWindow(QtWidgets.QMainWindow):
    # 封装类函数用以窗口跳转
    def __init__(self):  
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
    
    def setupUi(self, MainWindow):
        # 设置主窗口基本设定
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 436)
        MainWindow.setWindowIcon(QtGui.QIcon('./img/b.jpg'))
        MainWindow.setStyleSheet("#MainWindow{border-image:url(./img/b.jpg)}")
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # 设置主窗口内容
        self.title = QtWidgets.QLabel(parent=self.centralwidget)
        self.title.setGeometry(QtCore.QRect(280, 0, 301, 101))
        self.title.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.title.setScaledContents(False)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")
        self.title_w = QtWidgets.QLabel(parent=self.centralwidget)
        self.title_w.setGeometry(QtCore.QRect(-55, 10, 441, 71))
        self.title_w.setObjectName("title_w")
        MainWindow.setCentralWidget(self.centralwidget)

        # 创建工具栏
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        
        # 创建action
        self.actione = QtGui.QAction(parent=MainWindow)
        self.actione.setObjectName("actione")
        self.actione.triggered.connect(self.trans_E)
        self.actiond = QtGui.QAction(parent=MainWindow)
        self.actiond.setObjectName("actiond")
        self.actiond.triggered.connect(self.trans_D)
        self.action_show = QtGui.QAction(parent=MainWindow)
        self.action_show.setObjectName("action_show")
        self.action_show.triggered.connect(self.trans_bf)
        
        # 工具栏加入三个action
        self.toolBar.addAction(self.actione)
        self.toolBar.addAction(self.actiond)
        self.toolBar.addAction(self.action_show)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        # 设置显示的内容
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "主页"))
        self.title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:72pt; font-weight:700;\">S-DES</span></p></body></html>"))
        self.title_w.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:30pt; font-weight:500;\">Welcome to: </span></p></body></html>"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actione.setText(_translate("MainWindow", "加密"))
        self.actiond.setText(_translate("MainWindow", "解密"))
        self.action_show.setText(_translate("MainWindow", "暴力破解"))

    def trans_D(self):  
        # 解密窗口跳转
        self.ddd = dpage.Ui_Formd()
        self.ddd.show()

    def trans_E(self):  
        # 加密窗口跳转
        self.eee = epage.Ui_Forme()
        self.eee.show()

    def trans_bf(self):
        # 暴力破解窗口跳转
        self.bf = bfdepage.Ui_Formbf()
        self.bf.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #实例化主窗口
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
