# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simuNum.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_simu_input(object):
    def setupUi(self, simu_input):
        simu_input.setObjectName("simu_input")
        simu_input.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("shinnku.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        simu_input.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(simu_input)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(simu_input)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.simple_n = QtWidgets.QLineEdit(self.layoutWidget)
        self.simple_n.setObjectName("simple_n")
        self.horizontalLayout.addWidget(self.simple_n)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.multi_n = QtWidgets.QLineEdit(self.layoutWidget1)
        self.multi_n.setObjectName("multi_n")
        self.horizontalLayout_2.addWidget(self.multi_n)
        self.layoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.judge_n = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.judge_n.setObjectName("judge_n")
        self.horizontalLayout_3.addWidget(self.judge_n)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(simu_input)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(simu_input)
        self.buttonBox.accepted.connect(simu_input.accept) # type: ignore
        self.buttonBox.rejected.connect(simu_input.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(simu_input)

    def retranslateUi(self, simu_input):
        _translate = QtCore.QCoreApplication.translate
        simu_input.setWindowTitle(_translate("simu_input", "输入题目数量"))
        self.label.setText(_translate("simu_input", "单选题数量："))
        self.label_2.setText(_translate("simu_input", "多选题数量："))
        self.label_3.setText(_translate("simu_input", "判断题数量："))
