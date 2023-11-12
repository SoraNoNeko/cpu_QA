import copy

from PyQt5 import QtCore, QtGui, QtWidgets

import simuNum
import singleNum
import listManager
import cache
import file_deal


current_item = 0
adr_cache = cache.csv_adr


class ui_simu_input(simuNum.Ui_simu_input):
    def setupUi(self, simu_input):
        super(ui_simu_input, self).setupUi(simu_input)
        self.simple_n.setValidator(QtGui.QIntValidator())  # 设置只能输入int类型的数据
        self.multi_n.setValidator(QtGui.QIntValidator())
        self.judge_n.setValidator(QtGui.QIntValidator())
        self.buttonBox.accepted.connect(self.get_data)

    def get_data(self):
        sim = self.simple_n.text()
        multi = self.multi_n.text()
        judge = self.judge_n.text()
        if not sim:
            sim = "0"
        if not multi:
            multi = "0"
        if not judge:
            judge = "0"
        cache.simuNum = [int(sim), int(multi), int(judge)]


class ui_single_input(singleNum.Ui_single_input):
    def setupUi(self, single_input):
        super(ui_single_input, self).setupUi(single_input)
        self.lineEdit.setValidator(QtGui.QIntValidator())
        self.buttonBox.accepted.connect(self.get_data)

    def get_data(self):
        single = self.lineEdit.text()
        if not single:
            single = "0"
        cache.singleNum = [int(single)]


class ui_list_manager(listManager.Ui_Dialog):
    def __init__(self):
        super(ui_list_manager, self).__init__()
        self.dialog = None

    def setupUi(self, Dialog):
        super(ui_list_manager, self).setupUi(Dialog)
        self.dialog = Dialog
        self.addButton.clicked.connect(self.list_add)
        self.delButton.clicked.connect(self.list_del)
        self.buttonBox.accepted.connect(self.list_update)
        self.dataList.itemClicked.connect(self.list_select)
        self.list_load()

    def list_load(self):
        if len(adr_cache) > 1:
            for i in adr_cache:
                if i == 0:
                    continue
                self.dataList.addItem(i.text())
                self.dataList.viewport().update()
            return 0
        else:
            return 1

    def list_add(self):
        fname, ftype = QtWidgets.QFileDialog.getOpenFileName(self.dialog, "选择题库", "./",
                                                             "CSV(*.csv)")  # 如果添加一个内容则需要加两个分号
        adr_cache.append(copy.deepcopy(file_deal.file_(fname, self.dataList.count()+1)))
        self.dataList.addItem(adr_cache[-1].text())
        self.dataList.viewport().update()

    def list_del(self):
        global current_item
        if current_item == 0:
            return 1
        adr_cache.pop(current_item)
        for i in range(len(adr_cache)):
            if i == 0:
                continue
            adr_cache[i].code = i
        self.dataList.clear()
        self.list_load()
        self.dataList.viewport().update()
        if current_item > self.dataList.count():
            current_item = self.dataList.count()
        return 0

    @staticmethod
    def list_select(item):
        global current_item
        current_item = int(item.text()[1])

    def list_update(self):
        cache.csv_adr = adr_cache
        cache.csv_current = current_item
        try:
            file_deal.csv_deal()
        except:
            self.list_del()
            cache.mention = 1
        return 0
