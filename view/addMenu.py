import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import *
# 引用UI文件，根据设计的界面类型选择继承窗口类型，如：QMainWindow -> Ui_MainWindow,QWidget->Ui_Form,QDialog同样
from widget.ui_addMenu import Ui_Dialog_addMenu
from database.connector import Connector


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class AddMenu(QDialog, Ui_Dialog_addMenu):
    # 结束对话框
    switch_menuManageForAdmin = pyqtSignal()
    update_table = pyqtSignal()

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super(AddMenu, self).__init__(parent)
        self.setupUi(self)  # 设置界面
        self.retranslateUi(self)
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
        # 默认选择不是招牌菜
        self.radioButton_nospesial.setChecked(True)
        # 默认选择饮品
        self.radioButton_drink.setChecked(True)
        # 点击"确定添加"按钮
        self.pushButton_sureAdd.clicked.connect(self.on_click_SureAddMenuButton)
        # 点击"退出"按钮
        self.pushButton_quit.clicked.connect(self.on_click_QuitButton)

    # 增加菜品
    def on_click_SureAddMenuButton(self):
        # 检查数据是否填完 数据是否合法
        food_name, food_price, food_type, food_info, is_spesial = self.checkData()
        cursor = self.conn.get_cursor()
        sql = 'INSERT INTO `food_info` (f_name, price, t_id, food_info, is_special) VALUES (%s, %s, %s, %s, %s);'
        cursor.execute(sql, (food_name, food_price, food_type, food_info, is_spesial))
        self.conn.get_connection()
        # 执行完后关闭自身页面
        self.switch_menuManageForAdmin.emit()


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
    window = AddMenu()
    # 展示窗口
    window.show()
    app.exec()
