import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_adminLogin import Ui_MainWindow_adminLogin
from database.connector import Connector


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class AdminLogin(QMainWindow, Ui_MainWindow_adminLogin):
    switch_firstWindow = pyqtSignal()
    switch_manageForWindow = pyqtSignal()

    def __init__(self, parent=None):
        """

        :param parent:
        """
        super(AdminLogin, self).__init__(parent)
        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        # 设置数据库
        self.conn = Connector()
        # 自定义初始化函数
        self.initUI()

    def initUI(self):
        """
        # 自定义初始化函数
        #
        :return:
        """
        # 设置默认用户名
        self.lineEdit_userName.setText("钱自娟")
        # 设置默认密码
        # 如何设置密码隐藏
        self.lineEdit_password.setText("999999999")
        # 点击"登录"按钮
        self.pushButton_adminLogin.clicked.connect(self.on_click_LoginButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    def on_click_LoginButton(self):
        """
        点击”登录“按钮
        进行登录验证
        若成功则跳转
        :return:
        """
        # 从登录框中获取数据
        username = self.lineEdit_userName.text()
        password = self.lineEdit_password.text()
        if username == '':
            QMessageBox.warning(self, "出错了", "用户名不能为空！")
            return
        if password == '':
            QMessageBox.warning(self, "出错了", "密码不能为空！")
            return
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT a_id FROM `admin_info` WHERE a_name = %s AND password = %s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()
        if result is None:
            QMessageBox.critical(self, '登录失败', '用户名或密码错误，请重试')
            return
        # 界面跳转
        # 跳转至管理员管理界面
        self.switch_manageForWindow.emit()


    def on_click_QuitButton(self):
        """
        点击取消按钮
        退回主界面
        :return:
        """
        self.switch_firstWindow.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminLogin()
    # 展示窗口
    window.show()
    app.exec()
