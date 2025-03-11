import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_firstWindow import Ui_MainWindow_first


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class FirstWindow(QMainWindow, Ui_MainWindow_first):
    # 界面跳转
    # 跳转至顾客登录界面
    switch_customWindow = pyqtSignal()
    # 跳转至管理员登录界面
    switch_adminWindow = pyqtSignal()

    def __init__(self, parent=None):
        """
        """
        super(FirstWindow, self).__init__(parent)
        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        # 自定义初始化函数
        self.initUI()

    def initUI(self):
        """
        # 自定义初始化函数
        #
        :return:
        """
        # 点击"顾客"按钮
        self.pushButton_custom.clicked.connect(self.on_click_CustomButton)
        # 点击"管理员"按钮
        self.pushButton_admin.clicked.connect(self.on_click_AdminButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    def on_click_CustomButton(self):
        """
        点击”顾客“按钮
        跳转到顾客页面
        :return:
        """
        self.switch_customWindow.emit()

    def on_click_AdminButton(self):
        """
        点击”管理员“按钮
        跳转到管理员页面
        :return:
        """
        self.switch_adminWindow.emit()

    def on_click_QuitButton(self):
        """
        点击退出按钮
        :return:
        """
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FirstWindow()
    # 展示窗口
    window.show()
    app.exec()
