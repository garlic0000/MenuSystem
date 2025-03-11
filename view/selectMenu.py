import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import *
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_selectMenu import Ui_Dialog_selectMenu
from database.connector import Connector
from lib.share import Share


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class SelectMenu(QDialog, Ui_Dialog_selectMenu):
    # 结束对话框
    switch_menuForCustom = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(SelectMenu, self).__init__(parent)

        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        self.h_table_header = ['名称', '价格', '种类', '是否招牌菜', '介绍']
        # 禁止编辑
        self.tableWidget_selectMenu.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置最后一列占满
        self.tableWidget_selectMenu.horizontalHeader().setStretchLastSection(True)
        # 设置表格的选取方式是行选取
        self.tableWidget_selectMenu.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.special_group = QButtonGroup()
        self.special_group.addButton(self.radioButton_special)
        self.special_group.addButton(self.radioButton_nospecial)
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
        # 默认设置
        self.checkBox_foodName.setChecked(False)
        self.checkBox_foodType.setChecked(False)
        self.checkBox_foodPrice.setChecked(False)
        self.checkBox_isSpecial.setChecked(False)
        self.radioButton_special.setChecked(True)
        # 点击"查询顾客"按钮
        self.pushButton_selectMenu.clicked.connect(self.on_click_SelectMenuButton)
        # 点击"取消"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    # 增加菜品
    def on_click_SelectMenuButton(self):
        # 检查数据是否填完 数据是否合法
        cursor = self.conn.get_cursor()
        sql = 'SELECT f_name, price, t_id, is_special, food_info FROM `food_info`'
        sql_conclusion = []
        conclusion = []
        # 处理菜品类型
        sql_sub_conclusion = []
        sub_conclusion = []
        if self.checkBox_foodName.isChecked() is False and self.checkBox_foodPrice.isChecked() is False and self.checkBox_foodType.isChecked() is False and self.checkBox_isSpecial.isChecked() is False:
            QMessageBox.warning(self, '注意', '请至少选择一个查询条件!')
            return
        if self.checkBox_foodName.isChecked():
            if self.lineEdit_foodName == '':
                QMessageBox.warning(self, '注意', '用户名不能为空!')
                return
            sql_conclusion.append('f_name = %s')
            conclusion.append(self.lineEdit_foodName.text())
        if self.checkBox_foodPrice.isChecked():
            if self.lineEdit_foodPriceSmall == '' or self.lineEdit_foodPriceBig == '':
                QMessageBox.warning(self, '注意', '价格区间不能为空!')
                return
            if float(self.lineEdit_foodPriceSmall.text()) < 0:
                QMessageBox.warning(self, '注意', '请输入正确的价格区间!')
                return
            sql_conclusion.append('(price >= %s AND price <= %s)')
            conclusion.append(float(self.lineEdit_foodPriceSmall.text()))
            conclusion.append(float(self.lineEdit_foodPriceBig.text()))
        if self.checkBox_foodType.isChecked():
            if self.checkBox_drink.isChecked() is False and self.checkBox_soup.isChecked() is False and self.checkBox_coldDish.isChecked() is False and self.checkBox_chafingDish.isChecked() is False and self.checkBox_friedDish.isChecked() is False:
                QMessageBox.warning(self, '注意', '请至少选择一个菜品种类!')
                return
            if self.checkBox_drink.isChecked():
                sql_sub_conclusion.append('t_id = %s')
                sub_conclusion.append(1)
            if self.checkBox_soup.isChecked():
                sql_sub_conclusion.append('t_id = %s')
                sub_conclusion.append(2)
            if self.checkBox_coldDish.isChecked():
                sql_sub_conclusion.append('t_id = %s')
                sub_conclusion.append(3)
            if self.checkBox_chafingDish.isChecked():
                sql_sub_conclusion.append('t_id = %s')
                sub_conclusion.append(4)
            if self.checkBox_friedDish.isChecked():
                sql_sub_conclusion.append('t_id = %s')
                sub_conclusion.append(5)
        if self.checkBox_isSpecial.isChecked():
            sql_conclusion.append('is_special = %s')
            if self.radioButton_special.isChecked():
                conclusion.append(True)
            else:
                conclusion.append(False)
        str_sql_conclusion = " AND ".join(sql_conclusion)
        str_sql_sub_conclusion = " OR ".join(sql_sub_conclusion)
        if len(str_sql_conclusion) == 0 and len(str_sql_sub_conclusion) > 0:
            sql = sql + ' WHERE ' + str_sql_sub_conclusion + ';'
        elif len(str_sql_sub_conclusion) == 0 and len(str_sql_conclusion) > 0:
            sql = sql + ' WHERE ' + str_sql_conclusion + ';'
        elif len(str_sql_conclusion) > 0 and len(str_sql_sub_conclusion) == 1:
            sql = sql + ' WHERE ' + str_sql_conclusion + ' AND ' + str_sql_sub_conclusion + ';'
        else:
            sql = sql + ' WHERE ' + str_sql_conclusion + ' AND ' + '(' + str_sql_sub_conclusion + ')' + ';'
        conclusion = tuple(conclusion + sub_conclusion)
        cursor.execute(sql, conclusion)
        result = cursor.fetchall()
        # print(result)
        # (('西红柿炒鸡蛋', 26.0, 5, 0, '色泽鲜艳，酸甜爽口，口感爽滑，色香味浓'),)
        if len(result) == 0:
            self.tableWidget_selectMenu.setRowCount(0)
            return
        row = len(result)  # 行数
        col = len(result[0])  # 列数
        self.tableWidget_selectMenu.setRowCount(row)
        self.tableWidget_selectMenu.setColumnCount(col)
        self.tableWidget_selectMenu.setHorizontalHeaderLabels(self.h_table_header)
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
                self.tableWidget_selectMenu.setItem(i, j, item)


    def on_click_QuitButton(self):
        """
        点击取消按钮
        返回主界面
        :return:
        """
        self.switch_menuForCustom.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectMenu()
    # 展示窗口
    window.show()
    app.exec()
