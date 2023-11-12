import os

import cache


fname = cache.csv_adr[cache.csv_current]
# fname = ["题库（请勿重命名）.csv"]


class question:
    def __init__(self, num: int, ques, ans, option=None, finish=0):
        if option is None:
            option = []
        self.num = num
        self.ques = ques
        self.ans = ans
        self.option = option
        self.finish = finish
        # 1 单选 2 多选 3 判断
        if len(ans) > 1:
            self.type = 2
        elif ans in ["Y", "N"]:
            self.type = 3
        else:
            self.type = 1


class file_:
    def __init__(self, adr: str, code=0):
        self.adr = adr
        self.code = code

    def text(self):
        return "["+str(self.code)+"]"+self.adr[self.adr.rindex("/")+1:]


def csv_deal():
    global fname
    fname = cache.csv_adr[cache.csv_current]
    if fname:
        if os.path.exists(fname.adr):
            cache.close = 0
            csv_load()
        else:
            cache.close = 1
    else:
        cache.close = 1


def csv_load():
    lt = []
    with open(fname.adr, "rt", encoding='ANSI') as a:
        for line in a:
            lt.append(line.strip().split(","))
    n = 0
    for item in lt:
        cache.question.append(question(n, item[0], item[-1] if len(item[-1]) > 0 else item[1],
                                       [item[1], item[2], item[3], item[4]] if len(item[-1]) > 0 else []))
    for ques in cache.question:
        if ques.type == 1:
            cache.single.append(ques)
        elif ques.type == 2:
            cache.multi.append(ques)
        elif ques.type == 3:
            cache.judge.append(ques)
