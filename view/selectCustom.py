import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import *
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_selectCustom import Ui_Dialog_selectCustom
from database.connector import Connector
from lib.share import Share


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class SelectCustom(QDialog, Ui_Dialog_selectCustom):
    # 结束对话框
    switch_customListForAdmin = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(SelectCustom, self).__init__(parent)

        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        self.h_table_header = ['用户名', '手机号']
        # 禁止编辑
        self.tableWidget_customList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 每列占满
        self.tableWidget_customList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置表格的选取方式是行选取
        self.tableWidget_customList.setSelectionBehavior(QAbstractItemView.SelectRows)
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
        # 默认不选中
        self.checkBox_customName.setChecked(False)
        self.checkBox_phonenumber.setChecked(False)
        # 点击"查询顾客"按钮
        self.pushButton_selectCustom.clicked.connect(self.on_click_SelectCustomButton)
        # 点击"取消"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    # 增加菜品
    def on_click_SelectCustomButton(self):
        # 检查数据是否填完 数据是否合法
        cursor = self.conn.get_cursor()
        if self.checkBox_customName.isChecked() and self.checkBox_phonenumber.isChecked():
            username = self.lineEdit_customName.text()
            phonenumber = self.lineEdit_phonenumber.text()
            if username == '':
                QMessageBox.warning(self, '注意', '用户名不能为空!')
                return
            if phonenumber == '':
                QMessageBox.warning(self, '注意', '手机号码不能为空!')
                return
            sql = 'SELECT c_name, phone_number FROM `custom_info` WHERE c_name=%s AND phone_number=%s;'
            cursor.execute(sql, (username, phonenumber))
        elif self.checkBox_customName.isChecked():
            username = self.lineEdit_customName.text()
            if username == '':
                QMessageBox.warning(self, '注意', '用户名不能为空!')
                return
            sql = 'SELECT c_name, phone_number FROM `custom_info` WHERE c_name=%s;'
            cursor.execute(sql, username)
        elif self.checkBox_phonenumber.isChecked():
            phonenumber = self.lineEdit_phonenumber.text()
            if phonenumber == '':
                QMessageBox.warning(self, '注意', '手机号码不能为空!')
                return
            sql = 'SELECT c_name, phone_number FROM `custom_info` WHERE phone_number=%s;'
            cursor.execute(sql, phonenumber)
        else:
            QMessageBox.warning(self, '注意', '请至少选择一个查询条件!')
            return
        result = cursor.fetchall()
        if len(result) == 0:
            self.tableWidget_customList.setRowCount(0)
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_customList.setRowCount(row)
        self.tableWidget_customList.setColumnCount(col)
        self.tableWidget_customList.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(row):
            for j in range(col):
                item = QTableWidgetItem()
                item.setText(result[i][j])
                self.tableWidget_customList.setItem(i, j, item)


    def on_click_QuitButton(self):
        """
        点击取消按钮
        返回主界面
        :return:
        """
        self.switch_customListForAdmin.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectCustom()
    # 展示窗口
    window.show()
    app.exec()
