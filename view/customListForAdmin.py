import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import *
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_customListForAdmin import Ui_MainWindow_customListForAdmin
from database.connector import Connector
from lib.share import Share


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class CustomListForAdmin(QMainWindow, Ui_MainWindow_customListForAdmin):
    # 跳转至管理员管理页面
    switch_manageForAdmin = pyqtSignal()
    # 弹出删除顾客对话框
    switch_deleteCustom = pyqtSignal()
    # 弹出查询对话框
    switch_selectCustom = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(CustomListForAdmin, self).__init__(parent)
        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        self.h_table_header = ['用户名', '手机号码']
        # 禁止编辑
        self.tableWidget_customTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 最后一列占满表格
        # https://blog.csdn.net/can3981132/article/details/115258216
        # 设置每列都占满
        self.tableWidget_customTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置表格的选取方式是行选取
        self.tableWidget_customTable.setSelectionBehavior(QAbstractItemView.SelectRows)

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
        # 显示菜单数据
        self.show_customTable()
        # 点击"删除菜品"按钮
        self.pushButton_deleteCustom.clicked.connect(self.on_click_DeleteCustomButton)
        # 点击"查询菜单"按钮
        self.pushButton_showCustom.clicked.connect(self.on_click_SelectMenuButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    # 删除顾客
    def on_click_DeleteCustomButton(self):
        row_select = self.tableWidget_customTable.selectedItems()
        if len(row_select) == 0:
            QMessageBox.warning(self, "注意", "请选中要删除的顾客!")
            return
        row_list = []
        for i in range(len(row_select)):
            row_list.append(row_select[i].text())
        Share.row_list_for_delete = row_list
        self.switch_deleteCustom.emit()

    # 查询顾客
    def on_click_SelectMenuButton(self):
        self.switch_selectCustom.emit()

    # 显示招牌菜
    def show_customTable(self):
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT c_name, phone_number FROM `custom_info`"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        if result is None:
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_customTable.setRowCount(row)
        self.tableWidget_customTable.setColumnCount(col)
        self.tableWidget_customTable.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(len(result)):
            for j in range(len(result[0])):
                item = QTableWidgetItem()
                item.setText(str(result[i][j]))
                self.tableWidget_customTable.setItem(i, j, item)

    def on_click_QuitButton(self):
        """
        点击取消按钮
        返回主界面
        :return:
        """
        # self.close()
        self.switch_manageForAdmin.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomListForAdmin()
    # 展示窗口
    window.show()
    app.exec()
