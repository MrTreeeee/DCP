import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
import calculator
import functions
import numpy as np
import re
from PyQt5.QtGui import QIcon


def strnum2mat(line_edit):
    trans_str = np.mat(list(map(int, line_edit.split())))

    return trans_str


def equal_clicked():
    # 先获取两个输入字符串
    d_et = ui.dice_edit.text()
    g_et = ui.goal_edit.text()

    # 检查输入是否异常
    tmp = 0
    d_list = d_et.split()
    l_d = len(d_list)  # 数字个数
    correct_form = re.compile(r"^[1-9][0-9]*$")
    for i in range(l_d):
        if re.match(correct_form, d_list[i]):
            tmp += 1

    # 确认第一个位置的输入符合格式 并且 第二个位置的输入是正整数
    if tmp == l_d and re.match(correct_form, g_et):
        d_mat = strnum2mat(d_et)
        d_num = functions.before_unpack(d_mat)[0]
        d_face = functions.before_unpack(d_mat)[1]
        inner_prod = np.inner(d_num, d_face)[0, 0]

        # 确认第一个位置的输入不会过大 并且 第二个位置的输入合理
        if inner_prod > 300 or int(g_et) < d_num.sum() or int(g_et) > inner_prod:
            ui.prob_label.setText('Reject!')
        else:
            dice_mat = strnum2mat(ui.dice_edit.text())
            goal = int(ui.goal_edit.text())
            pr = functions.cal_p(dice_mat, goal)
            ui.prob_label.setText('{:.2f}'.format(100 * pr) + '%')
    else:
        ui.prob_label.setText('Reject!')


def bigger_clicked():
    # 先获取两个输入字符串
    d_et = ui.dice_edit.text()
    g_et = ui.goal_edit.text()

    # 检查输入是否异常
    tmp = 0
    d_list = d_et.split()
    l_d = len(d_list)  # 数字个数
    correct_form = re.compile(r"^[1-9][0-9]*$")
    for i in range(l_d):
        if re.match(correct_form, d_list[i]):
            tmp += 1

    # 确认第一个位置的输入符合格式 并且 第二个位置的输入是正整数
    if tmp == l_d and re.match(correct_form, g_et):
        d_mat = strnum2mat(d_et)
        d_num = functions.before_unpack(d_mat)[0]
        d_face = functions.before_unpack(d_mat)[1]
        inner_prod = np.inner(d_num, d_face)[0, 0]

        # 确认第一个位置的输入不会过大 并且 第二个位置的输入合理
        if inner_prod > 300 or int(g_et) < d_num.sum() or int(g_et) > inner_prod:
            ui.prob_label.setText('Reject!')
        else:
            dice_mat = strnum2mat(ui.dice_edit.text())
            goal = int(ui.goal_edit.text())
            pr = functions.sum_p(dice_mat, goal)
            ui.prob_label.setText('{:.2f}'.format(100 * pr) + '%')
    else:
        ui.prob_label.setText('Reject!')


app = QApplication(sys.argv)

window = QMainWindow()

ui = calculator.Ui_MainWindow()
ui.setupUi(window)
window.setWindowIcon(QIcon('R-C.jpg'))
window.show()

ui.equal_button.clicked.connect(equal_clicked)
ui.bigger_button.clicked.connect(bigger_clicked)

sys.exit(app.exec_())
