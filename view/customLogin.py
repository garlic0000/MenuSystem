import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_customLogin import Ui_MainWindow_customLogin
from database.connector import Connector


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class CustomLogin(QMainWindow, Ui_MainWindow_customLogin):
    # 跳转至注册界面
    switch_registerWindow = pyqtSignal()
    # 跳转至菜单界面
    switch_menuForCustom = pyqtSignal()
    # 跳转至主界面
    switch_firstWindow = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(CustomLogin, self).__init__(parent)
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
        # 点击"登录"按钮
        self.pushButton_Login.clicked.connect(self.on_click_LoginButton)
        # 点击"注册"按钮
        self.pushButton_customRegister.clicked.connect(self.on_click_RegisterButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    def on_click_LoginButton(self):
        """
        点击”登录“按钮
        进行登录验证
        若成功则跳转
        :return:
        """
        username = self.lineEdit_userName.text()
        password = self.lineEdit_password.text()
        phonenumber = self.lineEdit_phoneNumber.text()
        if username == '':
            QMessageBox.warning(self, "出错了", "用户名不能为空！")
            return
        if password == '':
            QMessageBox.warning(self, "出错了", "密码不能为空！")
            return
        if phonenumber == '':
            QMessageBox.warning(self, "出错了", "手机号码不能为空！")
            return
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT c_id FROM `custom_info` WHERE c_name = %s AND password = %s AND phone_number = %s"
        cursor.execute(sql, (username, password, phonenumber))
        result = cursor.fetchone()
        if result is None:
            QMessageBox.warning(self, '登录失败', '用户名或密码或手机号码错误，请重试')
            return
        QMessageBox.information(self, "登录成功", "欢迎用户{}".format(username))
        # 界面跳转
        # 跳转至顾客菜单界面
        self.switch_menuForCustom.emit()

    def on_click_RegisterButton(self):
        """
        点击”注册“按钮
        跳转到注册页面
        :return:
        """
        self.switch_registerWindow.emit()

    def on_click_QuitButton(self):
        """
        点击取消按钮
        返回主界面
        :return:
        """
        # self.close()
        self.switch_firstWindow.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomLogin()
    # 展示窗口
    window.show()
    app.exec()
