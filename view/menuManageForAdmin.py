import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import *
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_menuManageForAdmin import Ui_MainWindow_menuManage
from database.connector import Connector
from lib.share import Share


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class MenuManageForAdmin(QMainWindow, Ui_MainWindow_menuManage):
    # 跳转至管理员管理界面
    switch_manageForAdmin = pyqtSignal()
    # 弹出增加菜品对话框
    switch_addMenu = pyqtSignal()
    # 弹出修改菜品对对话框
    switch_modifyMenu = pyqtSignal()
    # 弹出删除菜品对话框
    switch_deleteMenu = pyqtSignal()
    # 弹出查询菜品对话框
    switch_selectMenu = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(MenuManageForAdmin, self).__init__(parent)
        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        self.h_table_header = ['名称', '价格', '种类', '是否招牌菜', '介绍']
        # 禁止编辑
        self.tableWidget_menu.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 最后一列占满表格
        # https://blog.csdn.net/can3981132/article/details/115258216
        # 设置最后一列占满
        self.tableWidget_menu.horizontalHeader().setStretchLastSection(True)
        # 设置表格的选取方式是行选取
        self.tableWidget_menu.setSelectionBehavior(QAbstractItemView.SelectRows)
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
        self.show_menuTable()
        # 点击"增加菜品"按钮
        self.pushButton_addMenu.clicked.connect(self.on_click_AddMenuButton)
        # 点击"删除菜品"按钮
        self.pushButton_deleteMenu.clicked.connect(self.on_click_DeleteMenuButton)
        # 点击"修改菜品"按钮
        self.pushButton_modifyMenu.clicked.connect(self.on_click_ModifyMenuButton)
        # 点击"查询菜单"按钮
        self.pushButton_selectMenu.clicked.connect(self.on_click_SelectMenuButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    # 增加菜品
    def on_click_AddMenuButton(self):
        self.switch_addMenu.emit()

    # 删除菜品
    def on_click_DeleteMenuButton(self):
        row_select = self.tableWidget_menu.selectedItems()
        if len(row_select) == 0:
            QMessageBox.warning(self, "注意", "请选中要删除的菜品!")
            return
        row_list = []
        for i in range(len(row_select)):
            row_list.append(row_select[i].text())
        Share.row_list_for_delete = row_list
        self.switch_deleteMenu.emit()

    # 修改菜品
    def on_click_ModifyMenuButton(self):
        row_select = self.tableWidget_menu.selectedItems()
        if len(row_select) == 0:
            QMessageBox.warning(self, "注意", "请选中要修改的菜品!")
            return
        row_list = []
        for i in range(len(row_select)):
            row_list.append(row_select[i].text())
        Share.row_list_for_modify = row_list
        self.switch_modifyMenu.emit()

    # 查询菜品
    def on_click_SelectMenuButton(self):
        self.switch_selectMenu.emit()

    # 显示招牌菜
    def show_menuTable(self):
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT f_name, price, t_id, is_special, food_info FROM `food_info`"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        if result is None:
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_menu.setRowCount(row)
        self.tableWidget_menu.setColumnCount(col)
        self.tableWidget_menu.setHorizontalHeaderLabels(self.h_table_header)
        food_type = ['饮品', '汤类', '凉菜', '火锅', '炒菜']
        for i in range(len(result)):
            for j in range(len(result[0])):
                item = QTableWidgetItem()
                if j == 2:
                    # 查询种类
                    ans = food_type[result[i][j] - 1]
                elif j == 3:
                    # 判断是否为招牌菜
                    if result[i][j] == 1:
                        ans = '是'
                    else:
                        ans = '否'
                else:
                    ans = str(result[i][j])
                item.setText(ans)
                self.tableWidget_menu.setItem(i, j, item)

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
    window = MenuManageForAdmin()
    # 展示窗口
    window.show()
    app.exec()
