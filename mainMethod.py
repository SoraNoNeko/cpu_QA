import copy
import functools
import os
import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor

import mainWindow
import inputMethod
import file_deal
import random
import cache

answer = [0, 0, 0, 0]
total_ans = []
corr_ans = []
record = {"amount": 0, "correct": 0, "current": 0, "total": 0, "mode": 0}
achieve = {"amount": 0, "correct": 0}
questions = []
end = 0


class Ui_MainMethod(mainWindow.Ui_MainWindow):
    def __init__(self):
        super(Ui_MainMethod, self).__init__()
        self.selDi = None
        self.simuDi = None
        self.singDi = None
        self.statusBar_version = None
        self.MainWindow = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.ques_show("请选择左侧模式")
        # 信号与槽
        self.A_c.clicked.connect(self.A_clicked)
        self.B_c.clicked.connect(self.B_clicked)
        self.C_c.clicked.connect(self.C_clicked)
        self.D_c.clicked.connect(self.D_clicked)
        self.pushButton_1.clicked.connect(self.single_random)
        self.pushButton_2.clicked.connect(self.multi_random)
        self.pushButton_3.clicked.connect(self.judge_random)
        self.pushButton_4.clicked.connect(self.normal_mode)
        self.pushButton_5.clicked.connect(self.simulate_test)
        self.pushButton_6.clicked.connect(MainWindow.info)
        self.last_B.clicked.connect(self.ques_last)
        self.next_B.clicked.connect(self.ques_next)
        self.last_q.triggered.connect(self.ques_last)
        self.next_q.triggered.connect(self.ques_next)
        self.enter.clicked.connect(self.enter_ques)
        self.see.triggered.connect(self.wrong_record)
        self.clear.triggered.connect(self.wrong_clear)
        self.clear_all.triggered.connect(self.cl_all)
        self.actionAbout.triggered.connect(self.about)
        self.file_sel.triggered.connect(self.file_select)
        self.size_l.triggered.connect(self.size_large)
        self.size_m.triggered.connect(self.size_middle)
        self.size_s.triggered.connect(self.size_small)

        # 状态栏部件
        self.statusBar_version = QtWidgets.QLabel("刷题 v0.4.0")
        self.statusBar_version.setAlignment(QtCore.Qt.AlignRight)
        self.statusBar.addPermanentWidget(self.statusBar_version)
        self.status_add("当前题库：{0}".format(
            cache.csv_adr[cache.csv_current].text() if cache.csv_adr[cache.csv_current] else 0))

    # Method
    # A选项
    def A_clicked(self):
        answer[0] = self.A_c.isChecked()

    # B选项
    def B_clicked(self):
        answer[1] = self.B_c.isChecked()

    # C选项
    def C_clicked(self):
        answer[2] = self.C_c.isChecked()

    # D选项
    def D_clicked(self):
        answer[3] = self.D_c.isChecked()

    @staticmethod
    def reset():
        if cache.question:
            record["amount"] = 0
            record["current"] = 0
            record['correct'] = 0
            global end
            end = 0
            questions.clear()
            corr_ans.clear()
            total_ans.clear()
            questions.clear()
            return 1
        else:
            return 0

    # 单选
    def single_random(self):
        if self.reset():
            if cache.single:
                self.show_single()
                num = cache.singleNum[0]
                length = len(cache.single)
                if num <= 0:
                    self.MainWindow.show_message("提醒", "请输入正确的数字")
                    return 0
                if num >= length:
                    self.MainWindow.show_message("提醒", "超出题库大小")
                    return 0
                questions.extend(random.sample(cache.single, num))
                record["mode"] = 1
                record["total"] = num
                self.question_load()
            else:
                self.MainWindow.show_message("提醒", "题库中无单选题")
        else:
            self.mention_load()

    # 多选
    def multi_random(self):
        if self.reset():
            if cache.multi:
                self.show_single()
                num = cache.singleNum[0]
                length = len(cache.multi)
                if num <= 0:
                    self.MainWindow.show_message("提醒", "请输入正确的数字")
                    return 0
                if num >= length:
                    self.MainWindow.show_message("提醒", "超出题库大小")
                    return 0
                questions.extend(random.sample(cache.multi, num))
                record["mode"] = 2
                record["total"] = num
                self.question_load()
            else:
                self.MainWindow.show_message("提醒", "题库中无多选题")
        else:
            self.mention_load()

    # 判断
    def judge_random(self):
        if self.reset():
            if cache.judge:
                self.show_single()
                num = cache.singleNum[0]
                length = len(cache.judge)
                if num <= 0:
                    self.MainWindow.show_message("提醒", "请输入正确的数字")
                    return 0
                if num >= length:
                    self.MainWindow.show_message("提醒", "超出题库大小")
                    return 0
                questions.extend(random.sample(cache.judge, num))
                record["mode"] = 3
                record["total"] = num
                self.question_load()
            else:
                self.MainWindow.show_message("提醒", "题库中无判断题")
        else:
            self.mention_load()

    # 顺序
    def normal_mode(self):
        if self.reset():
            questions.extend(cache.question)
            record["mode"] = 4
            record["total"] = len(cache.question)
            self.question_load()
        else:
            self.mention_load()

    # 模拟
    def simulate_test(self):
        self.reset()
        self.show_simu()
        num = cache.simuNum
        n = 0
        kun = ["单选题", "多选题", "判断题"]
        item = dict(zip(num, [cache.single, cache.multi, cache.judge]))
        for x, y in item.items():
            length = len(y)
            if x <= 0:
                self.MainWindow.show_message("提醒", "{}请输入正确的数字".format(kun[n]))
                self.show_simu()
                return 0
            if x >= length:
                self.MainWindow.show_message("提醒", "{}超出题库大小".format(kun[n]))
                self.show_simu()
                return 0
            n = n + 1

        questions.extend(random.sample(cache.single, num[0]))
        questions.extend(random.sample(cache.multi, num[1]))
        questions.extend(random.sample(cache.judge, num[2]))
        record["mode"] = 5
        record["total"] = sum(num)
        self.question_load()

    # 错题记录
    def wrong_record(self):
        if cache.wrong:
            self.reset()
            questions.extend(cache.wrong)
            record["mode"] = 6
            record["total"] = len(cache.wrong)
            self.question_load()
        else:
            self.MainWindow.show_message("提醒", "目前没有错题")

    # 错题清除
    def wrong_clear(self):
        cache.wrong.clear()
        self.MainWindow.show_message("提醒", "错题记录清除成功")

    # 清除所有记录
    def cl_all(self):
        cache.wrong.clear()
        global answer, total_ans, corr_ans, record, achieve, questions, end
        answer = [0, 0, 0, 0]
        total_ans = []
        corr_ans = []
        record = {"amount": 0, "correct": 0, "current": 0, "total": 0, "mode": 0}
        achieve = {"amount": 0, "correct": 0}
        questions = []
        end = 0
        save_var([answer, total_ans, corr_ans, record, achieve, questions, end], "data0.dat")
        save_var([cache.wrong, cache.csv_adr, cache.csv_current, cache.font_size], "data1.dat")
        self.ques_show("")
        self.mention("")
        self.A_c.setChecked(0)
        self.B_c.setChecked(0)
        self.C_c.setChecked(0)
        self.D_c.setChecked(0)
        self.MainWindow.show_message("提醒", "清除记录成功")

    # 关于信息
    def about(self):
        self.MainWindow.show_message("关于", "Developed by 二阶堂真红\nQQ：3069838783\n根据张凯杰同学软件修改完成")

    # 题目载入
    def question_load(self, ans=None):
        if ans is None:
            ans = [0, 0, 0, 0]
        self.mention("")
        if record["mode"] == 0:
            self.A_c.setChecked(ans[0])
            self.B_c.setChecked(ans[1])
            self.C_c.setChecked(ans[2])
            self.D_c.setChecked(ans[3])
            self.A_c.setCheckable(True)
            self.B_c.setCheckable(True)
            self.C_c.setCheckable(True)
            self.D_c.setCheckable(True)
            self.A_c.setAutoExclusive(True)
            self.B_c.setAutoExclusive(True)
            self.C_c.setAutoExclusive(True)
            self.D_c.setAutoExclusive(True)
            self.A_b.setText("A")
            self.B_b.setText("B")
            self.C_b.setText("C")
            self.D_b.setText("D")
            return 0
        self.enter.setText("提交")
        self.enter.setEnabled(True)
        ques = questions[record.get("current")]
        if ques.type == 1:
            self.ques_show("""第{0}题\n{1}\nA {2}\nB {3}\nC {4}\nD {5}\n""".format((record["current"] + 1),
                                                                                 ques.ques,
                                                                                 ques.option[0],
                                                                                 ques.option[1],
                                                                                 ques.option[2],
                                                                                 ques.option[3]
                                                                                 ))
            self.A_c.setAutoExclusive(False)
            self.B_c.setAutoExclusive(False)
            self.C_c.setAutoExclusive(False)
            self.D_c.setAutoExclusive(False)
            self.A_c.setChecked(ans[0])
            self.B_c.setChecked(ans[1])
            self.C_c.setChecked(ans[2])
            self.D_c.setChecked(ans[3])
            self.A_c.setAutoExclusive(True)
            self.B_c.setAutoExclusive(True)
            self.C_c.setAutoExclusive(True)
            self.D_c.setAutoExclusive(True)
            self.A_c.setCheckable(True)
            self.B_c.setCheckable(True)
            self.C_c.setCheckable(True)
            self.D_c.setCheckable(True)
            self.A_b.setText("A")
            self.B_b.setText("B")
            self.C_b.setText("C")
            self.D_b.setText("D")
        elif ques.type == 2:
            self.ques_show("""第{0}题\n{1}\nA {2}\nB {3}\nC {4}\nD {5}\n""".format((record["current"] + 1),
                                                                                 ques.ques,
                                                                                 ques.option[0],
                                                                                 ques.option[1],
                                                                                 ques.option[2],
                                                                                 ques.option[3]
                                                                                 ))
            self.A_c.setAutoExclusive(False)
            self.B_c.setAutoExclusive(False)
            self.C_c.setAutoExclusive(False)
            self.D_c.setAutoExclusive(False)
            self.A_c.setChecked(ans[0])
            self.B_c.setChecked(ans[1])
            self.C_c.setChecked(ans[2])
            self.D_c.setChecked(ans[3])
            self.A_c.setCheckable(True)
            self.B_c.setCheckable(True)
            self.C_c.setCheckable(True)
            self.D_c.setCheckable(True)
            self.A_b.setText("A")
            self.B_b.setText("B")
            self.C_b.setText("C")
            self.D_b.setText("D")
        elif ques.type == 3:
            self.ques_show("""第{0}题\n{1}\n""".format((record["current"] + 1), ques.ques))
            self.A_c.setAutoExclusive(False)
            self.B_c.setAutoExclusive(False)
            self.C_c.setAutoExclusive(False)
            self.D_c.setAutoExclusive(False)
            self.A_c.setChecked(ans[0])
            self.B_c.setChecked(ans[1])
            self.C_c.setChecked(ans[2])
            self.D_c.setChecked(ans[3])
            self.A_c.setAutoExclusive(True)
            self.B_c.setAutoExclusive(True)
            self.C_c.setAutoExclusive(True)
            self.D_c.setAutoExclusive(True)
            self.A_c.setCheckable(True)
            self.B_c.setCheckable(True)
            self.C_c.setCheckable(False)
            self.D_c.setCheckable(False)
            self.A_b.setText("True")
            self.B_b.setText("False")
            self.C_b.setText("")
            self.D_b.setText("")

    # 上文本框显示
    def ques_show(self, context: str):
        self.question.setText(context)

    # 下文本框显示
    def mention(self, context: str):
        self.answer.setText(context)

    def check_op(self):
        global answer
        answer = [0] * 4
        answer[0] = self.A_c.isChecked()
        answer[1] = self.B_c.isChecked()
        answer[2] = self.C_c.isChecked()
        answer[3] = self.D_c.isChecked()

    def ques_next(self):
        if record["mode"] == 0:
            self.MainWindow.show_message("提醒", "请选择左侧答题模式")
            return 0
        self.mention("")
        if record["current"] + 1 == record["total"]:
            self.MainWindow.show_message("提醒", "已经到最后一题了")
            return 0
        if record['mode'] == 5:
            self.enter_ques()
            if record["current"] + 1 == len(total_ans):
                record["current"] = record["current"] + 1
                if record["amount"] + 1 == record["total"]:
                    self.enter.setText("交卷")
                self.question_load()
                return 0
            elif record["current"] + 1 < len(total_ans):
                record["current"] = record["current"] + 1
                if record["amount"] + 1 == record["total"]:
                    self.enter.setText("交卷")
                self.question_load(ans=total_ans[record["current"]])
                if end == 1:
                    self.ans_jud()
                return 0
        if questions[record["current"]].finish == 0:
            self.enter_ques()
            return 0
        if record["current"] + 1 == len(total_ans):
            record["current"] = record["current"] + 1
            self.question_load()
            return 0
        elif record["current"] + 1 < len(total_ans):
            record["current"] = record["current"] + 1
            self.question_load(ans=total_ans[record["current"]])
            self.ans_jud()
            return 0

    def ques_last(self):
        if record["mode"] == 0:
            self.MainWindow.show_message("提醒", "请选择左侧答题模式")
            return 0
        self.mention("")
        if record["current"] == 0:
            self.MainWindow.show_message("提醒", "已经到第一题了")
            return 0
        if record['mode'] == 5:
            self.enter_ques()
            record["current"] = record["current"] - 1
            if record["amount"] + 1 == record["total"]:
                self.enter.setText("交卷")
            self.question_load(ans=total_ans[record["current"]])
            if end == 1:
                self.ans_jud()
            return 0
        else:
            record["current"] = record["current"] - 1
            self.question_load(ans=total_ans[record["current"]])
            self.ans_jud()
            return 0

    def enter_ques(self):
        if record["mode"] == 0:
            self.MainWindow.show_message("提醒", "请选择左侧答题模式")
            return 0
        if record['mode'] == 4 or record['mode'] == 6 or record['mode'] == 1 or record['mode'] == 2 or record[
            'mode'] == 3:
            if questions[record["current"]].finish == 0:
                if self.ans_jud():
                    record["correct"] = record["correct"] + 1
                    achieve["correct"] = achieve["correct"] + 1
                    questions[record["current"]].finish = 1
                else:
                    if not record["mode"] == 6:
                        cache.wrong.append(copy.deepcopy(questions[record["current"]]))
                    questions[record["current"]].finish = 1
                total_ans.append(copy.deepcopy(answer))
                record["amount"] = record["amount"] + 1
                achieve["amount"] = achieve["amount"] + 1
                self.status_add("当前题库：{0}，共{1}道，已做{2}道，正确{3}道".format(
                    cache.csv_adr[cache.csv_current].text() if cache.csv_adr[cache.csv_current] else 0,
                    record["total"], record["amount"],
                    record["correct"]))
                return 0
            else:
                self.ans_jud()
                return 0
        elif record['mode'] == 5:
            self.check_op()
            if questions[record["current"]].finish:
                total_ans[record["current"]] = answer
                corr_ans[record["current"]] = self.ans_deal(questions[record.get("current")])
            else:
                total_ans.append(copy.deepcopy(answer))
                corr_ans.append(copy.deepcopy(questions[record.get("current")].ans))
                record["amount"] = record["amount"] + 1
                questions[record["current"]].finish = 1
            if record["amount"] == record["total"]:
                self.mention("答题结束，答题情况：")
                corr = 0
                for i in range(len(total_ans)):
                    if total_ans[i] == corr_ans[i]:
                        self.question.moveCursor(QTextCursor.End)
                        self.question.insertPlainText("第{0}题，正确 ".format(i))
                        corr = corr + 1
                        achieve["correct"] = achieve["correct"] + 1
                    else:
                        self.question.moveCursor(QTextCursor.End)
                        self.question.insertPlainText("第{0}题，错误 ".format(i))
                        cache.wrong.append(copy.deepcopy(questions[i]))
                    achieve["amount"] = achieve["amount"] + 1
                    if i % 5 == 4:
                        self.question.append("")
                self.question.append("")
                self.question.append("共{0}题，正确{1}道题 ".format(record["total"], corr))
                self.enter.setCheckable(False)
                global end
                end = 1
            self.status_add("当前题库{2}，共{0}道，已做{1}道".format(record["total"], record["amount"],
                                                          cache.csv_adr[cache.csv_current].text() if cache.csv_adr[
                                                              cache.csv_current] else 0))
            return 0

    @staticmethod
    def ans_deal(ques):
        _answer = [0, 0, 0, 0]
        if "A" in ques.ans:
            _answer[0] = 1
        if "B" in ques.ans:
            _answer[1] = 1
        if "C" in ques.ans:
            _answer[2] = 1
        if "D" in ques.ans:
            _answer[3] = 1
        if "Y" in ques.ans:
            _answer = [1, 0, 0, 0]
        if "N" in ques.ans:
            _answer = [0, 1, 0, 0]
        return _answer

    def ans_jud(self):
        self.check_op()
        _answer = self.ans_deal(questions[record["current"]])
        if answer == _answer:
            self.mention("答案正确")
            return 1
        else:
            self.mention("答案错误,正确答案为：{}".format(questions[record["current"]].ans))
            return 0

    def status_add(self, context: str):
        QtWidgets.QStatusBar.showMessage(self.statusBar, context, 3600000)

    # 初始化 包括载入上次进度和载入题库
    def initial(self):
        # 缓存初始化
        if os.path.exists("data0.dat") and os.path.exists("data0.dat"):
            data0 = load_var("data0.dat")
            data1 = load_var("data1.dat")
            global answer, total_ans, corr_ans, record, achieve, questions, end
            answer, total_ans, corr_ans, record, achieve, questions, end = data0
            cache.wrong, cache.csv_adr, cache.csv_current, cache.font_size = data1
            if record["mode"] == 0:
                self.A_c.setChecked(0)
                self.B_c.setChecked(0)
                self.C_c.setChecked(0)
                self.D_c.setChecked(0)
                file_deal.csv_deal()
                return 0

            self.question_load()
            if len(total_ans) > record["current"]:
                self.A_c.setChecked(total_ans[record["current"]][0])
                self.B_c.setChecked(total_ans[record["current"]][1])
                self.C_c.setChecked(total_ans[record["current"]][2])
                self.D_c.setChecked(total_ans[record["current"]][3])
                file_deal.csv_deal()
                return 0
            else:
                self.A_c.setChecked(0)
                self.B_c.setChecked(0)
                self.C_c.setChecked(0)
                self.D_c.setChecked(0)
                file_deal.csv_deal()
                return 0
        self.font_size(cache.font_size)
        try:
            file_deal.csv_deal()
        except:
            self.MainWindow.show_message("注意", """题库加载失败，请检查题库是否符合格式
                            格式说明：
                            单选多选：题干,A选项,B选项,C选项,D选项,答案
                            判断：题干,答案,,,,
                            暂时只支持四选项选择题""")
        if cache.close:
            self.mention_load()

    def file_select(self):
        self.selDi = QtWidgets.QDialog()
        self.selDi.setWindowModality(QtCore.Qt.ApplicationModal)
        d = inputMethod.ui_list_manager()
        d.setupUi(self.selDi)
        self.selDi.show()
        self.selDi.exec_()

    def mention_load(self):
        a = QtWidgets.QMessageBox.warning(self.MainWindow, "提醒", "题库未选择\n是否选择题库", QtWidgets.QMessageBox.Yes |
                                          QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if a == QtWidgets.QMessageBox.Yes:
            self.file_select()
            if cache.mention == 1:
                self.MainWindow.show_message("注意", """题库加载失败，请检查题库是否符合格式
                                格式说明：
                                单选多选：题干,A选项,B选项,C选项,D选项,答案
                                判断：题干,答案,,,,
                                暂时只支持四选项选择题""")

    def show_single(self):
        self.singDi = QtWidgets.QDialog()
        self.singDi.setWindowModality(QtCore.Qt.ApplicationModal)
        d = inputMethod.ui_single_input()
        d.setupUi(self.singDi)
        self.singDi.show()
        self.singDi.exec_()

    def show_simu(self):
        self.simuDi = QtWidgets.QDialog()
        self.simuDi.setWindowModality(QtCore.Qt.ApplicationModal)
        d = inputMethod.ui_simu_input()
        d.setupUi(self.simuDi)
        self.simuDi.show()
        self.simuDi.exec_()

    def font_size(self, f_type: int):
        if f_type == 1:  # small
            cache.font_size = 1
            self.question.setFontPointSize(9)
            self.answer.setFontPointSize(9)
        elif f_type == 2:  # middle
            cache.font_size = 2
            self.question.setFontPointSize(12)
            self.answer.setFontPointSize(12)
        elif f_type == 3:  # large
            cache.font_size = 3
            self.question.setFontPointSize(15)
            self.answer.setFontPointSize(15)
        self.question_load()

    def size_small(self):
        self.font_size(1)

    def size_middle(self):
        self.font_size(2)

    def size_large(self):
        self.font_size(3)

    """
    def ques_next(self):
        if record["mode"] == 0:
            self.MainWindow.show_message("提醒", "请选择左侧答题模式")
            return 0
        self.mention("")
        if record["current"] < record["total"] - 1:
            if record["current"] == record["amount"] - 1 or record["current"] == record["amount"]:
                if questions[record["current"]].finish == 1:
                    record["current"] = record["current"] + 1
                    self.question_load()
                    self.A_c.setChecked(0)
                    self.B_c.setChecked(0)
                    self.C_c.setChecked(0)
                    self.D_c.setChecked(0)
                    answer.clear()
                    answer.extend([0, 0, 0, 0])
                else:
                    self.enter_ques()
            else:
                record["current"] = record["current"] + 1
                self.question_load()
                self.A_c.setChecked(total_ans[record["current"]][0])
                self.B_c.setChecked(total_ans[record["current"]][1])
                self.C_c.setChecked(total_ans[record["current"]][2])
                self.D_c.setChecked(total_ans[record["current"]][3])
        else:
            self.MainWindow.show_message("提醒", "已经到最后一题了")

    def ques_last(self):
        if record["mode"] == 0:
            self.MainWindow.show_message("提醒", "请选择左侧答题模式")
            return 0
        self.mention("")
        if record["current"] > 0:
            record["current"] = record["current"] - 1
            self.question_load()
            self.A_c.setChecked(total_ans[record["current"]][0])
            self.B_c.setChecked(total_ans[record["current"]][1])
            self.C_c.setChecked(total_ans[record["current"]][2])
            self.D_c.setChecked(total_ans[record["current"]][3])
        else:
            self.MainWindow.show_message("提醒", "已经到第一题了")
"""


"""    
    def enter_ques(self):
        if record["mode"] == 0:
            self.MainWindow.show_message("提醒", "请选择左侧答题模式")
            return 0
        self.check_op()
        global end
        if questions[record["current"]].finish == 0 or end == 1:
            if end == 0:
                record["amount"] = record["amount"] + 1
                achieve["amount"] = achieve["amount"] + 1
                _answer = [0, 0, 0, 0]
                ques = questions[record.get("current")]
                if "A" in ques.ans:
                    _answer[0] = 1
                if "B" in ques.ans:
                    _answer[1] = 1
                if "C" in ques.ans:
                    _answer[2] = 1
                if "D" in ques.ans:
                    _answer[3] = 1
                if "Y" in ques.ans:
                    _answer = [1, 0, 0, 0]
                if "N" in ques.ans:
                    _answer = [0, 1, 0, 0]
                if record['mode'] == 4 or record['mode'] == 6 or record['mode'] == 1 or record['mode'] == 2 or 
                    record['mode'] == 3:
                    if len(total_ans) > record["current"]:
                        total_ans[record["current"]] = _answer
                    else:
                        total_ans.append(_answer)
                        corr_ans.append(questions[record.get("current")].ans)
                    if answer == _answer:
                        record["correct"] = record["correct"] + 1
                        achieve["correct"] = achieve["correct"] + 1
                        self.mention("答案正确")

                    else:
                        cache.wrong.append(questions[record["current"]])
                        self.mention("答案错误,正确答案为：{}".format(questions[record.get("current")].ans))
                    questions[record["current"]].finish = 1
                    self.status_add("共{0}道，已做{1}道，正确{2}道".format(record["total"], record["amount"], 
                                    record["correct"]))
                if record['mode'] == 5:
                    if len(total_ans) > record["current"]:
                        total_ans[record["current"]] = _answer
                    else:
                        total_ans.append(_answer)
                        corr_ans.append(questions[record.get("current")].ans)
                    self.status_add("共{0}道，已做{1}道".format(record["total"], record["amount"]))
                    questions[record["current"]].finish = 1
                if record["amount"] == record["total"]:
                    self.enter.setText("交卷")
                    end = 1
            else:
                if record['mode'] == 4 or record['mode'] == 6 or record['mode'] == 1 or record['mode'] == 2 or 
                    record['mode'] == 3:
                    self.ques_show("答题结束，共{0}道，正确{1}道".format(record["total"], record["correct"]))
                elif record['mode'] == 5:
                    self.mention("答题结束，答题情况：")
                    corr = 0
                    for i in range(len(total_ans)):
                        if total_ans[i] == corr_ans[i]:
                            self.question.moveCursor(QTextCursor.End)
                            self.question.insertPlainText("第{0}题，正确 ".format(i))
                            corr = corr + 1
                        else:
                            self.question.moveCursor(QTextCursor.End)
                            self.question.insertPlainText("第{0}题，错误 ".format(i))
                            cache.wrong.append(questions[i])
                        if i % 5 == 4:
                            self.question.append("")
                    self.question.append("")
                    self.question.append("共{0}题，正确{1}道题 ".format(len(total_ans), corr))
                    self.enter.setText("提交")
                    self.enter.setCheckable(False)
"""


class MyWidgets(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWidgets, self).__init__()
        self.setWindowIcon(QtGui.QIcon("shinnku.ico"))

    def closeEvent(self, event):  # 关闭窗口触发以下事件
        if cache.close == 1:
            event.accept()
            app = QtWidgets.QApplication.instance()
            app.quit()
        else:
            a = QtWidgets.QMessageBox.question(self, '退出', '你确定要退出吗?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)  # "退出"代表的是弹出框的标题,"你确认退出.."表示弹出框的内容
            if a == QtWidgets.QMessageBox.Yes:
                save_var([answer, total_ans, corr_ans, record, achieve, questions, end], "data0.dat")
                save_var([cache.wrong, cache.csv_adr, cache.csv_current, cache.font_size], "data1.dat")
                event.accept()  # 接受关闭事件
            else:
                event.ignore()  # 忽略关闭事件

    # 弹窗
    def show_message(self, title: str, context: str):
        QtWidgets.QMessageBox.information(self, title, context,
                                          QtWidgets.QMessageBox.Ok)

    # 统计信息
    def info(self):
        self.show_message("统计信息", "共做{0}道题，正确{1}道题\n当前题库:{2}，其中共{3}道题，{4}道单选题，{5}道多选题，{6}道判断题".
                          format(achieve["amount"], achieve["correct"], cache.csv_adr[cache.csv_current].text(),
                                 len(cache.question), len(cache.single), len(cache.multi), len(cache.judge)))


# 缓存变量到本地
def save_var(v, filename):
    f = open(filename, 'wb')
    pickle.dump(v, f)
    f.close()
    return filename


def load_var(filename):
    f = open(filename, 'rb')
    re = pickle.load(f)
    f.close()
    return re
