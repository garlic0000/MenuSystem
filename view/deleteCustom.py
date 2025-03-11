import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import *
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_deleteCustom import Ui_Dialog_deleteCustom
from database.connector import Connector
from lib.share import Share


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class DeleteCustom(QDialog, Ui_Dialog_deleteCustom):
    # 关闭对话框
    switch_customListForAdmin = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(DeleteCustom, self).__init__(parent)

        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        # 读取数据
        self.row_list = Share.row_list_for_delete
        # 顾客在数据库中对应的编号
        self.c_id = 0
        self.h_table_header = ['用户名', '手机号']
        # 禁止编辑
        self.tableWidget_deleteRow.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置每列都占满
        self.tableWidget_deleteRow.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置表格的选取方式是行选取
        self.tableWidget_deleteRow.setSelectionBehavior(QAbstractItemView.SelectRows)
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
        # 显示待删除的行的信息
        self.show_deleteRow()
        # 点击"确定删除"按钮
        self.pushButton_sureDelete.clicked.connect(self.on_click_SureDeleteCustomButton)
        # 点击"取消"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    # 增加菜品
    def on_click_SureDeleteCustomButton(self):
        # 检查数据是否填完 数据是否合法
        cursor = self.conn.get_cursor()
        sql = 'DELETE FROM `custom_info` WHERE c_id=%s;'
        cursor.execute(sql, self.c_id)
        # 重新连接
        self.conn.get_connection()
        # 执行完后关闭自身页面
        self.switch_customListForAdmin.emit()

    def show_deleteRow(self):
        # 设置显示信息
        cursor = self.conn.get_cursor()
        sql = 'SELECT c_id FROM `custom_info` WHERE phone_number=%s;'
        cursor.execute(sql, (self.row_list[1]))
        result = cursor.fetchone()
        self.c_id = result[0]
        row = 1  # 行数
        col = len(self.row_list)  # 列数
        self.tableWidget_deleteRow.setRowCount(row)
        self.tableWidget_deleteRow.setColumnCount(col)
        self.tableWidget_deleteRow.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(row):
            for j in range(col):
                item = QTableWidgetItem()
                item.setText(self.row_list[j])
                self.tableWidget_deleteRow.setItem(i, j, item)

    def on_click_QuitButton(self):
        """
        点击取消按钮
        返回主界面
        :return:
        """
        self.switch_customListForAdmin.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeleteCustom()
    # 展示窗口
    window.show()
    app.exec()
