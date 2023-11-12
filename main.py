import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import mainMethod
import file_deal
import cache

if __name__ == '__main__':

    # 获取UIC窗口操作权限
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = mainMethod.MyWidgets()
    # 调自定义的界面（即刚转换的.py对象）
    Ui = mainMethod.Ui_MainMethod()
    Ui.setupUi(MainWindow)
    Ui.initial()
    # 显示窗口并释放资源
    MainWindow.show()
    sys.exit(app.exec_())
