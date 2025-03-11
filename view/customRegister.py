import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_customRegister import Ui_MainWindow_customRegister
from database.connector import Connector


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class CustomRegister(QMainWindow, Ui_MainWindow_customRegister):
    # 跳转至登录界面
    switch_customLoginWindow = pyqtSignal()

    def __init__(self, parent=None):
        """

        :param parent:
        """
        super(CustomRegister, self).__init__(parent)
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
        # 点击"注册"按钮
        self.pushButton_register.clicked.connect(self.on_click_RegisterButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    def on_click_RegisterButton(self):
        """
        点击”注册“按钮
        若注册成功
        跳转到登录页面
        :return:
        """
        username = self.lineEdit_userName.text()
        password = self.lineEdit_password.text()
        passwordSure = self.lineEdit_passwordSure.text()
        phonenumber = self.lineEdit_phoneNumber.text()
        if username == '':
            QMessageBox.warning(self, "出错了", "用户名不能为空！")
            return
        if password == '':
            QMessageBox.warning(self, "出错了", "密码不能为空！")
            return
        if passwordSure == '':
            QMessageBox.warning(self, "出错了", "确认密码不能为空！")
            return
        if phonenumber == '':
            QMessageBox.warning(self, "出错了", "手机号码不能为空！")
            return
        if password != passwordSure:
            QMessageBox.warning(self, "出错了", "密码与确认密码不同!")
            return
        # 从数据库中查询手机号码
        cursor = self.conn.get_cursor()
        sql = "SELECT c_id FROM `custom_info` WHERE phone_number=%s"
        cursor.execute(sql, phonenumber)
        result = cursor.fetchone()
        if result is not None:
            QMessageBox.warning(self, '注册失败', '该手机号码已被注册')
            return
        # 插入顾客信息
        cursor = self.conn.get_cursor()
        sql = "INSERT INTO `custom_info` (c_name, password, phone_number) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password, phonenumber))
        self.conn.get_connection()
        QMessageBox.information(self, '注册成功', '用户{}注册成功'.format(username))
        # 界面跳转
        # 跳转至登录界面
        self.switch_customLoginWindow.emit()

    def on_click_QuitButton(self):
        """
        点击取消按钮
        退回登录界面
        :return:
        """
        self.switch_customLoginWindow.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomRegister()
    # 展示窗口
    window.show()
    app.exec()
