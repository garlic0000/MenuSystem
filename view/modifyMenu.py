import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import *
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_modifyMenu import Ui_Dialog_modifyMenu
from database.connector import Connector
from lib.share import Share


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class ModifyMenu(QDialog, Ui_Dialog_modifyMenu):
    # 结束后关闭对话框
    switch_menuManageForAdmin = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(ModifyMenu, self).__init__(parent)

        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
        # 读取数据
        self.row_list = Share.row_list_for_modify
        # 菜品在数据库中对应的编号
        self.f_id = 0
        self.food_type_group = QButtonGroup()
        self.food_type_group.addButton(self.radioButton_drink)
        self.food_type_group.addButton(self.radioButton_soup)
        self.food_type_group.addButton(self.radioButton_coldDish)
        self.food_type_group.addButton(self.radioButton_chafingDish)
        self.food_type_group.addButton(self.radioButton_friedDish)
        self.special_group = QButtonGroup()
        self.special_group.addButton(self.radioButton_spesial)
        self.special_group.addButton(self.radioButton_nospesial)
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
        # 将选中行的信息填入
        self.solveData()
        # 点击"确定修改"按钮
        self.pushButton_sureModify.clicked.connect(self.on_click_SureModifyMenuButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    # 增加菜品
    def on_click_SureModifyMenuButton(self):
        # 检查数据是否填完 数据是否合法
        food_name, food_price, food_type, food_info, is_spesial = self.checkData()
        cursor = self.conn.get_cursor()
        sql = 'UPDATE `food_info` SET f_name = %s, price = %s, t_id = %s, food_info = %s, is_special = %s WHERE f_id=%s;'
        cursor.execute(sql, (food_name, food_price, food_type, food_info, is_spesial, self.f_id))
        # 数据更新,页面重新显示
        self.conn.get_connection()
        # 执行完后关闭自身页面
        self.switch_menuManageForAdmin.emit()

    def solveData(self):
        # ['凉拌黄瓜', '14.0', '凉菜', '否', '香脆，爽口、酸、辣、甜、咸']
        # 设置显示信息
        cursor = self.conn.get_cursor()
        sql = 'SELECT f_id FROM `food_info` WHERE f_name=%s;'
        cursor.execute(sql, self.row_list[0])
        result = cursor.fetchone()
        self.f_id = result[0]
        self.lineEdit_foodName.setText(self.row_list[0])
        self.lineEdit_foodPrice.setText(self.row_list[1])
        food_types = {'饮品': self.radioButton_drink,
                      '汤类': self.radioButton_soup,
                      '凉菜': self.radioButton_coldDish,
                      '火锅': self.radioButton_chafingDish,
                      '炒菜': self.radioButton_friedDish}
        food_types[self.row_list[2]].setChecked(True)
        if self.row_list[3] == '是':
            self.radioButton_spesial.setChecked(True)
        else:
            self.radioButton_nospesial.setChecked(True)
        self.textEdit_foodInfo.setText(self.row_list[4])

    def checkData(self):
        # 检查数据是否为空
        food_name = self.lineEdit_foodName.text()
        food_price = self.lineEdit_foodPrice.text()
        food_info = self.textEdit_foodInfo.toPlainText()
        if food_name == '':
            QMessageBox.warning(self, "出错了", "菜品名称不能为空!")
            return
        if food_price == '':
            QMessageBox.warning(self, "出错了", "菜品价格不能为空!")
            return
        if food_info == '':
            QMessageBox.warning(self, "出错了", "菜品介绍不能为空!")
            return
        food_price = float(food_price)
        food_types = [self.radioButton_drink.isChecked(),
                      self.radioButton_soup.isChecked(),
                      self.radioButton_coldDish.isChecked(),
                      self.radioButton_chafingDish.isChecked(),
                      self.radioButton_chafingDish.isChecked()]
        food_type = 0
        for radio in food_types:
            food_type = food_type + 1
            if radio is True:
                break
        is_spesial = self.radioButton_spesial.isChecked()

        return food_name, food_price, food_type, food_info, is_spesial

    def on_click_QuitButton(self):
        """
        点击取消按钮
        返回主界面
        :return:
        """
        self.switch_menuManageForAdmin.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModifyMenu()
    # 展示窗口
    window.show()
    app.exec()
