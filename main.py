import sys
from PyQt5.QtWidgets import *
from view.firstWindow import FirstWindow
from view.customLogin import CustomLogin
from view.adminLogin import AdminLogin
from view.customRegister import CustomRegister
from view.menuForCustom import MenuForCustom
from view.manageForAdmin import ManageForAdmin
from view.menuManageForAdmin import MenuManageForAdmin
from view.addMenu import AddMenu
from view.deleteMenu import DeleteMenu
from view.modifyMenu import ModifyMenu
from view.customListForAdmin import CustomListForAdmin
from view.deleteCustom import DeleteCustom
from view.selectCustom import SelectCustom
from view.selectMenu import SelectMenu
from view.selectMenuForAdmin import SelectMenuForAdmin


# 利用一个控制器来控制页面的跳转
class Controller:
    def __init__(self):
        pass

    # 主窗口
    def show_firstWindow(self):
        self.firstWindow = FirstWindow()
        try:
            # 在用户登录界面 点击取消
            self.customLogin.close()
        except:
            pass
        try:
            # 在管理员登录界面 点击取消
            self.adminLogin.close()
        except:
            pass
        try:
            # 在顾客菜单界面 点击退出
            self.menuForCustom.close()
        except:
            pass
        try:
            # 在管理员管理界面 点击退出
            self.manageForAdmin.close()
        except:
            pass
        # 跳转到顾客登录界面
        self.firstWindow.switch_customWindow.connect(self.show_customLogin)
        # 跳转到管理员登录界面
        self.firstWindow.switch_adminWindow.connect(self.show_adminLogin)
        self.firstWindow.show()

    # 顾客登录窗口
    def show_customLogin(self):
        self.customLogin = CustomLogin()
        # 关闭主界面
        try:
            self.firstWindow.close()
        except:
            pass
        try:
            self.customRegister.close()
        except:
            pass
        # 点击注册 跳转到顾客注册界面
        self.customLogin.switch_registerWindow.connect(self.show_customRegister)
        # 点击登录 跳转至 顾客菜单界面
        self.customLogin.switch_menuForCustom.connect(self.show_menuForCustom)
        # 点击取消 跳转到主界面
        self.customLogin.switch_firstWindow.connect(self.show_firstWindow)
        self.customLogin.show()

    # 管理员登录界面
    def show_adminLogin(self):
        self.adminLogin = AdminLogin()
        try:
            self.firstWindow.close()
        except:
            pass
        # 跳转到管理员管理页面
        self.adminLogin.switch_manageForWindow.connect(self.show_manageForAdmin)
        # 跳转到主页面
        self.adminLogin.switch_firstWindow.connect(self.show_firstWindow)
        self.adminLogin.show()

    # 顾客注册界面
    def show_customRegister(self):
        self.customRegister = CustomRegister()
        try:
            self.customLogin.close()
        except:
            pass
        # 点击取消
        # 跳转至用户登录界面
        self.customRegister.switch_customLoginWindow.connect(self.show_customLogin)
        self.customRegister.show()

    # 顾客 菜单界面
    def show_menuForCustom(self):
        self.menuForCustom = MenuForCustom()
        try:
            # 用户登录界面 点击确定
            self.customLogin.close()
        except:
            pass
        try:
            self.selectMenu.close()
        except:
            pass
        # 点击取消 跳转至 主界面
        self.menuForCustom.switch_firstWindow.connect(self.show_firstWindow)
        # 点击查询 弹出查询界面
        self.menuForCustom.switch_selectMenuWindow.connect(self.show_selectMenu)
        # 显示菜单界面
        # 全屏显示
        self.menuForCustom.showMaximized()

    # 管理员管理页面
    def show_manageForAdmin(self):
        self.manageForAdmin = ManageForAdmin()
        try:
            # 主界面 点击管理员 主界面关闭
            self.firstWindow.close()
        except:
            pass
        try:
            self.adminLogin.close()
        except:
            pass
        try:
            self.menuManageForAdmin.close()
        except:
            pass
        try:
            # 在顾客管理界面 点击退出
            self.customListForAdmin.close()
        except:
            pass
        self.manageForAdmin.switch_menuManageWindow.connect(self.show_menuManageForAdmin)
        self.manageForAdmin.switch_customManageWindow.connect(self.show_customListForAdmin)
        self.manageForAdmin.switch_firstWindow.connect(self.show_firstWindow)
        self.manageForAdmin.show()

    # 管理员 菜单管理页面
    def show_menuManageForAdmin(self):
        self.menuManageForAdmin = MenuManageForAdmin()
        try:
            # 关闭管理员管理页面
            self.manageForAdmin.close()
        except:
            pass
        try:
            # 关闭增加菜品对话框
            self.addMenu.close()
        except:
            pass
        try:
            # 关闭删除菜品对话框
            self.deleteMenu.close()
        except:
            pass
        try:
            # 关闭修改菜品对话框
            self.modifyMenu.close()
        except:
            pass
        try:
            # 弹出查询菜品对话框
            self.selectMenuForAdmin.close()
        except:
            pass
        self.menuManageForAdmin.switch_addMenu.connect(self.show_addMenu)
        self.menuManageForAdmin.switch_deleteMenu.connect(self.show_deleteMenu)
        self.menuManageForAdmin.switch_modifyMenu.connect(self.show_modifyMenu)
        self.menuManageForAdmin.switch_selectMenu.connect(self.show_selectMenuForAdmin)
        self.menuManageForAdmin.switch_manageForAdmin.connect(self.show_manageForAdmin)
        self.menuManageForAdmin.show()

    def show_addMenu(self):
        self.addMenu = AddMenu()
        # 显示对话框的同时 菜单界面可同时存在
        self.addMenu.switch_menuManageForAdmin.connect(self.show_menuManageForAdmin)
        self.addMenu.show()

    def show_deleteMenu(self):
        self.deleteMenu = DeleteMenu()
        self.deleteMenu.switch_menuManageForAdmin.connect(self.show_menuManageForAdmin)
        self.deleteMenu.show()

    def show_modifyMenu(self):
        self.modifyMenu = ModifyMenu()
        self.modifyMenu.switch_menuManageForAdmin.connect(self.show_menuManageForAdmin)
        self.modifyMenu.show()

    # 管理员 顾客管理页面
    def show_customListForAdmin(self):
        self.customListForAdmin = CustomListForAdmin()
        try:
            # 关闭管理员管理页面
            self.manageForAdmin.close()
        except:
            pass
        try:
            # 关闭删除对话框
            self.deleteCustom.close()
        except:
            pass
        try:
            # 关闭查询对话框
            self.selectCustom.close()
        except:
            pass
        self.customListForAdmin.switch_deleteCustom.connect(self.show_deleteCustom)
        self.customListForAdmin.switch_selectCustom.connect(self.show_selectCustom)
        self.customListForAdmin.switch_manageForAdmin.connect(self.show_manageForAdmin)
        self.customListForAdmin.show()

    def show_deleteCustom(self):
        self.deleteCustom = DeleteCustom()
        self.deleteCustom.switch_customListForAdmin.connect(self.show_customListForAdmin)
        self.deleteCustom.show()

    def show_selectCustom(self):
        self.selectCustom = SelectCustom()
        self.selectCustom.switch_customListForAdmin.connect(self.show_customListForAdmin)
        self.selectCustom.show()

    def show_selectMenu(self):
        self.selectMenu = SelectMenu()
        self.selectMenu.switch_menuForCustom.connect(self.show_menuForCustom)
        self.selectMenu.show()

    def show_selectMenuForAdmin(self):
        self.selectMenuForAdmin = SelectMenuForAdmin()
        self.selectMenuForAdmin.switch_menuManageForAdmin.connect(self.show_menuManageForAdmin)
        self.selectMenuForAdmin.show()



def main():
    app = QApplication(sys.argv)
    controller = Controller()  # 控制器实例
    controller.show_firstWindow()  # 默认展示的是firstWindow页面
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
