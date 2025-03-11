import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import *
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_menuForCustom import Ui_MainWindow_menu
from database.connector import Connector


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class MenuForCustom(QMainWindow, Ui_MainWindow_menu):
    # 点击退出 跳转至主界面
    switch_firstWindow = pyqtSignal()
    # 点击查询菜品 弹出查询对话框
    switch_selectMenuWindow = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(MenuForCustom, self).__init__(parent)
        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        self.h_table_header = ['名称', '价格', '介绍']
        # 设置最后一列占满
        self.tableWidget_spesial.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_drink.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_soup.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_coldDishs.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_chafingDish.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_friedDish.horizontalHeader().setStretchLastSection(True)
        # 禁止编辑
        self.tableWidget_spesial.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_drink.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_soup.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_coldDishs.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_chafingDish.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_friedDish.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
        # 显示招牌菜数据
        self.show_spesialTable()
        # 显示饮品数据
        self.show_drinkTable()
        # 显示汤类数据
        self.show_soupTable()
        # 显示凉菜数据
        self.show_coldDishTable()
        # 显示炒菜数据
        self.show_friedDishTable()
        # 显示火锅数据
        self.show_chafingDishTable()
        # 点击 "查询菜品"按钮
        self.pushButton_selectMenu.clicked.connect(self.on_click_SelectMenuButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    # 显示招牌菜
    def show_spesialTable(self):
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT f_name, price, food_info  FROM `food_info` WHERE is_special=%s"
        cursor.execute(sql, 1)
        result = cursor.fetchall()
        if result is None:
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_spesial.setRowCount(row)
        self.tableWidget_spesial.setColumnCount(col)
        self.tableWidget_spesial.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(len(result)):
            for j in range(len(result[0])):
                item = QTableWidgetItem()
                item.setText(str(result[i][j]))
                self.tableWidget_spesial.setItem(i, j, item)

    # 显示饮品数据
    def show_drinkTable(self):
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT f_name, price, food_info  FROM `food_info` WHERE t_id=%s"
        cursor.execute(sql, 1)
        result = cursor.fetchall()
        # print(result)
        # (('image/ningmenghongcha.jpg', '柠檬红茶', 3.0, '具有柠檬的青酸与红茶的醇厚，茶汁微红、澄清，甜而微酸，十分爽口'),)
        if result is None:
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_drink.setRowCount(row)
        self.tableWidget_drink.setColumnCount(col)
        self.tableWidget_drink.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(len(result)):
            for j in range(len(result[0])):
                item = QTableWidgetItem()
                item.setText(str(result[i][j]))
                self.tableWidget_drink.setItem(i, j, item)

    # 显示汤类数据
    def show_soupTable(self):
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT f_name, price, food_info  FROM `food_info` WHERE t_id=%s"
        cursor.execute(sql, 2)
        result = cursor.fetchall()
        # print(result)
        # (('image/ningmenghongcha.jpg', '柠檬红茶', 3.0, '具有柠檬的青酸与红茶的醇厚，茶汁微红、澄清，甜而微酸，十分爽口'),)
        if result is None:
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_soup.setRowCount(row)
        self.tableWidget_soup.setColumnCount(col)
        self.tableWidget_soup.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(len(result)):
            for j in range(len(result[0])):
                item = QTableWidgetItem()
                item.setText(str(result[i][j]))
                # 图片不显示
                self.tableWidget_soup.setItem(i, j, item)

    # 显示凉菜
    def show_coldDishTable(self):
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT f_name, price, food_info  FROM `food_info` WHERE t_id=%s"
        cursor.execute(sql, 3)
        result = cursor.fetchall()
        # print(result)
        # (('image/ningmenghongcha.jpg', '柠檬红茶', 3.0, '具有柠檬的青酸与红茶的醇厚，茶汁微红、澄清，甜而微酸，十分爽口'),)
        if result is None:
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_coldDishs.setRowCount(row)
        self.tableWidget_coldDishs.setColumnCount(col)
        self.tableWidget_coldDishs.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(len(result)):
            for j in range(len(result[0])):
                item = QTableWidgetItem()
                item.setText(str(result[i][j]))
                self.tableWidget_coldDishs.setItem(i, j, item)

    # 显示火锅数据
    def show_chafingDishTable(self):
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT f_name, price, food_info  FROM `food_info` WHERE t_id=%s"
        cursor.execute(sql, 4)
        result = cursor.fetchall()
        # print(result)
        # (('image/ningmenghongcha.jpg', '柠檬红茶', 3.0, '具有柠檬的青酸与红茶的醇厚，茶汁微红、澄清，甜而微酸，十分爽口'),)
        if result is None:
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_chafingDish.setRowCount(row)
        self.tableWidget_chafingDish.setColumnCount(col)
        self.tableWidget_chafingDish.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(len(result)):
            for j in range(len(result[0])):
                item = QTableWidgetItem()
                item.setText(str(result[i][j]))
                # 图片不显示
                self.tableWidget_chafingDish.setItem(i, j, item)

    # 显示炒菜数据
    def show_friedDishTable(self):
        # 从数据库中查询信息
        cursor = self.conn.get_cursor()
        sql = "SELECT f_name, price, food_info  FROM `food_info` WHERE t_id=%s"
        cursor.execute(sql, 5)
        result = cursor.fetchall()
        # print(result)
        # (('image/ningmenghongcha.jpg', '柠檬红茶', 3.0, '具有柠檬的青酸与红茶的醇厚，茶汁微红、澄清，甜而微酸，十分爽口'),)
        if result is None:
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_friedDish.setRowCount(row)
        self.tableWidget_friedDish.setColumnCount(col)
        self.tableWidget_friedDish.setHorizontalHeaderLabels(self.h_table_header)
        for i in range(len(result)):
            for j in range(len(result[0])):
                item = QTableWidgetItem()
                item.setText(str(result[i][j]))
                # 图片不显示
                self.tableWidget_friedDish.setItem(i, j, item)

    def on_click_SelectMenuButton(self):
        # 点击查询按钮 弹出查询对话框
        self.switch_selectMenuWindow.emit()
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
    window = MenuForCustom()
    # 展示窗口
    # window.show()
    window.showMaximized()
    app.exec()
