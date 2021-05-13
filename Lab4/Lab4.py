import random
import numpy as np
from numpy.linalg import solve
from pprint import pprint
from scipy.stats import f, t
import time

N = 8
m = 8
x1_min, x2_min, x3_min = 15, 15, 15
x1_max, x2_max, x3_max = 45, 50, 30


y_min = 200 + round((x1_min + x2_min + x3_min) / 3)
y_max = 200 + round((x1_max + x2_max + x3_max) / 3)
print("y_min = " + str(y_min), "y_max = " + str(y_max))
print("")

mp = [[1, 1, 1, 1, 1, 1, 1, 1],
      [-1, -1, 1, 1, -1, -1, 1, 1],
      [-1, 1, -1, 1, -1, 1, -1, 1],
      [-1, 1, 1, -1, 1, -1, -1, 1]]
print("Матриця планування експерименту")
pprint(mp)
print("")

x1x2_norm = [0, 0, 0, 0, 0, 0, 0, 0]
x1x3_norm = [0, 0, 0, 0, 0, 0, 0, 0]
x2x3_norm = [0, 0, 0, 0, 0, 0, 0, 0]
x1x2x3_norm = [0, 0, 0, 0, 0, 0, 0, 0]
for i in range(N):
    x1x2_norm[i] = mp[1][i] * mp[2][i]
    x1x3_norm[i] = mp[1][i] * mp[3][i]
    x2x3_norm[i] = mp[2][i] * mp[3][i]
    x1x2x3_norm[i] = mp[1][i] * mp[2][i] * mp[3][i]
print("x1x2_norm= " + str(x1x2_norm), "x1x3_norm= " + str(x1x3_norm),
      "\nx2x3_norm= " + str(x2x3_norm), "x1x2x3_norm= " + str(x1x2x3_norm))
print("")

y1 = [random.randint(int(y_min), int(y_max)) for i in range(m)]
y2 = [random.randint(int(y_min), int(y_max)) for i in range(m)]
y3 = [random.randint(int(y_min), int(y_max)) for i in range(m)]

matrix_y = [[y1[0], y2[0], y3[0]],
            [y1[1], y2[1], y3[1]],
            [y1[2], y2[2], y3[2]],
            [y1[3], y2[3], y3[3]],
            [y1[4], y2[4], y3[4]],
            [y1[5], y2[5], y3[5]],
            [y1[6], y2[6], y3[6]],
            [y1[7], y2[7], y3[7]]]

print("Матриця планування Y")
pprint(matrix_y)
print("")

x0 = [1, 1, 1, 1, 1, 1, 1, 1]
x1 = [-10, -10, 50, 50, -10, -10, 50, 50]
x2 = [-20, 60, -20, 60, -20, 60, -20, 60]
x3 = [-20, 5, 5, -20, 5, -20, -20, 5]

x1x2 = [0, 0, 0, 0, 0, 0, 0, 0]
x1x3 = [0, 0, 0, 0, 0, 0, 0, 0]
x2x3 = [0, 0, 0, 0, 0, 0, 0, 0]
x1x2x3 = [0, 0, 0, 0, 0, 0, 0, 0]

for i in range(N):
    x1x2[i] = x1[i] * x2[i]
    x1x3[i] = x1[i] * x3[i]
    x2x3[i] = x2[i] * x3[i]
    x1x2x3[i] = x1[i] * x2[i] * x3[i]

aver_y = []
for i in range(len(matrix_y)):
    aver_y.append(np.mean(matrix_y[i], axis=0))

b_list = [mp[0], mp[1], mp[2], mp[3], x1x2_norm, x1x3_norm, x2x3_norm, x1x2x3_norm]
a_list = list(zip(x0, x1, x2, x3, x1x2, x1x3, x2x3, x1x2x3))

print("Матриця планування X")
pprint(a_list)
print("")

ai = [round(i, 3) for i in solve(a_list, aver_y)]
print("Рівняння регресії: \n" "y = {} + {}*x1 + {}*x2 + {}*x3 + {}*x1x2 + {}*x1x3 + {}*x2x3 + {}*x1x2x3".format(ai[0],
                                                                                                                ai[1],
                                                                                                                ai[2],
                                                                                                                ai[3],
                                                                                                                ai[4],
                                                                                                                ai[5],
                                                                                                                ai[6],
                                                                                                                ai[7]))
print("")

bi = []
for j in range(N):
    S = 0
    for i in range(N):
        S += (b_list[j][i] * aver_y[i]) / N
    bi.append(round(S, 3))
print("Рівняння регресії для нормованих факторів: \n" "y = {} + {}*x1 + {}*x2 + {}*x3 + {}*x1x2 + {}*x1x3 +"
      " {}*x2x3 + {}*x1x2x3".format(bi[0], bi[1], bi[2], bi[3], bi[4], bi[5], bi[6], bi[7]))
print("")

print("Перевірка за Кохреном")
print("")

print("Середні значення відгуку за рядками:", "\n", +aver_y[0], aver_y[1], aver_y[2], aver_y[3],
      aver_y[4], aver_y[5], aver_y[6], aver_y[7])
print("")
disp = []
for i in range(len(matrix_y)):
    a = 0
    for j in matrix_y[i]:
        a += (j - np.mean(matrix_y[i], axis=0)) ** 2
    disp.append(a / len(matrix_y[i]))
Gp = max(disp) / sum(disp)
Gt = 0.5157

if Gp < Gt:
    print("Дисперсія однорідна")
else:
    print("Дисперсія неоднорідна")
print("")

print("Перевірка за Стьюдентом")
sb = sum(disp) / len(disp)
sbs = (sb / (m * 3)) ** 0.5

t_list = [abs(bi[i]) / sbs for i in range(0, 8)]

d = 0
res = [0, 0, 0, 0, 0, 0, 0, 0]
coef_1 = []
coef_2 = []
mm = 3
F3 = (mm - 1) * N

for i in range(N):
    if t_list[i] < t.ppf(q=0.975, df=F3):
        coef_2.append(bi[i])
        res[i] = 0
    else:
        coef_1.append(bi[i])
        res[i] = bi[i]
        d += 1

print("Значущі коефіцієнти регресії:", coef_1)
print("Незначущі коефіцієнти регресії:", coef_2)

y_st = []
for i in range(N):
    y_st.append(res[0] + res[1] * mp[1][i] + res[2] * mp[2][i] + res[3] * mp[3][i] + res[4] * x1x2_norm[i]
                + res[5] * x1x3_norm[i] + res[6] * x2x3_norm[i] + res[7] * x1x2x3_norm[i])
print("Значення з отриманими коефіцієнтами:", y_st)
print("")

print("Перевірка за Фішером")
S_ad = mm * sum([(y_st[i] - aver_y[i]) ** 2 for i in range(8)]) / (N - d)
Fp = S_ad / sb
F4 = N - d
if Fp < f.ppf(q=0.95, dfn=F4, dfd=F3):
    print("При рівні значимості 0.05 рівняння регресії адекватне")
else:
    print("При рівні значимості 0.05 рівняння регресії неадекватне")

