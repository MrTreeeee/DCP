import math

import numpy as np

# 这是一个函数类, 包含 unpackmat, cal_p, sum_p 三个函数.
global dice_unpack, result_list, dice_sum


def unpackmat(repeat, value):  # 对于同一个位置 i , 把 value(i) 重复 repeat(i) 次, 遍历 i, 构成新矩阵 unpack
    s = np.zeros(shape=(1, 1))
    length = int(max(repeat.shape))
    for i in range(length):
        mid = np.ones(shape=(1, int(repeat[0, i]))) * value[0, i]
        s = np.append(np.array(s), np.array(mid))
    s = np.delete(s, 0)
    return np.mat(s)


def before_unpack(mat1):
    l_1 = max(mat1.shape)
    dice_num1 = np.zeros(shape=(1, int(l_1 / 2)))
    dice_face1 = np.zeros(shape=(1, int(l_1 / 2)))

    # 拆分输入的骰子矩阵, 将其拆成一个表示不同面数骰子数量 与 一个骰子各面的值的矩阵
    for i in range(int(l_1 / 2)):
        dice_num1[0, i] = mat1[0, 2 * i]
        dice_face1[0, i] = mat1[0, 2 * i + 1]

    return np.mat(np.append(np.array(dice_num1), np.array(dice_face1)).reshape(2, int(l_1 / 2)))


def cal_p(mat, goal):  # 接收一个骰子分布矩阵 mat 与 目标值 goal, 输出骰出 goal 的概率pr
    global dice_unpack, result_list, dice_sum
    dice_num = before_unpack(mat)[0]
    dice_face = before_unpack(mat)[1]

    dice_sum = dice_num.sum()  # 骰子总数 & 全局最小点数
    dice_max = np.multiply(dice_num, dice_face).sum()  # 全局最大点数

    dice_unpack = unpackmat(dice_num, dice_face)  # 拿到最终的解包矩阵

    # 定义一个存储了结果表中第 i 行的非零元素最大位置矩阵
    l_2 = int(max(dice_unpack.shape))  # 骰子数量
    all_max = np.zeros(shape=(1, l_2))
    all_max[0, 0] = dice_unpack[0, 0]
    for i in range(1, l_2):
        all_max[0, i] = all_max[0, i - 1] + dice_unpack[0, i]
    all_max -= 1  # 把元素从数值意义变成 python 位置意义

    result_list = np.zeros(shape=(int(dice_sum), int(dice_max)))  # 最终概率表的初始状态

    # 先对表的第一行赋值(递归的最终状态)
    for j in range(int(dice_max)):
        if j < dice_unpack[0, 0]:
            result_list[0, j] = 1
        else:
            result_list[0, j] = 0

    for i in range(1, int(dice_sum)):
        m = (all_max[0, i] + i) / 2  # 计算列表第 i 行非零元素位置的对称轴
        for j in range(int(dice_max)):
            if j <= all_max[0, i]:
                if j < i:  # 对角线下方填 0
                    result_list[i, j] = 0
                elif i <= j <= dice_unpack[0, i]:  # 没有超出该行骰子面数就从上一行第一个位置累加
                    t = 0
                    for k in range(j):
                        t += result_list[i - 1, k]
                    result_list[i, j] = t
                    # print(result_list)
                elif dice_unpack[0, i] < j <= math.floor(m):  # 超出该行骰子面数并且位于对称轴左侧, 将上一行初始相加位置向右移动
                    t = 0
                    for k in range(j - int(dice_unpack[0, i]), j):
                        t += result_list[i - 1, k]
                    result_list[i, j] = t
                else:  # 超出对称轴直接对称取值
                    result_list[i, j] = result_list[i, int(2 * m - j)]
            else:
                result_list[i, j] = 0

    all_possible = dice_unpack.prod()
    pr = result_list[int(dice_sum) - 1, goal - 1] / all_possible

    return pr


def sum_p(mat, goal):  # 接收一个骰子分布矩阵 mat 与 目标值 goal, 输出骰出不小于 goal 的概率Pr
    l_1 = int(max(mat.shape))
    num = np.zeros(shape=(1, int(l_1 / 2)))
    face = np.zeros(shape=(1, int(l_1 / 2)))

    for i in range(int(l_1 / 2)):
        num[0, i] = mat[0, 2 * i]
        face[0, i] = mat[0, 2 * i + 1]

    total = np.multiply(num, face).sum()
    pr = 0
    for i in range(goal, int(total) + 1):
        pr += cal_p(mat, i)

    return pr

