import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_manageForAdmin import Ui_MainWindow_manageForAdmin


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class ManageForAdmin(QMainWindow, Ui_MainWindow_manageForAdmin):
    # 界面跳转
    # 跳转至菜单管理界面
    switch_menuManageWindow = pyqtSignal()
    # 跳转至用户管理界面
    switch_customManageWindow = pyqtSignal()
    # 跳转至主界面
    switch_firstWindow = pyqtSignal()

    def __init__(self, parent=None):
        """
        """
        super(ManageForAdmin, self).__init__(parent)
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
        # 点击"顾客管理"按钮
        self.pushButton_customManage.clicked.connect(self.on_click_CustomManageButton)
        # 点击"菜单管理"按钮
        self.pushButton_menuManage.clicked.connect(self.on_click_MenuManageButton)
        # 点击"取消"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    def on_click_CustomManageButton(self):
        """
        跳转至顾客管理界面
        :return:
        """
        self.switch_customManageWindow.emit()

    def on_click_MenuManageButton(self):
        """
        跳转至菜单管理界面
        :return:
        """
        self.switch_menuManageWindow.emit()

    def on_click_QuitButton(self):
        """
        点击取消按钮
        # 跳转至主界面
        :return:
        """
        self.switch_firstWindow.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManageForAdmin()
    # 展示窗口
    window.show()
    app.exec()
