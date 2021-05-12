import random as r
import math
import sys

#test

rows = 3
variant = 5
m = 6
y_max = (30 - variant) * 10
y_min = (20 - variant) * 10
x1_min, x1_max, x2_min, x2_max = -30, 20, 25, 45
x1_min_norm, x1_max_norm = -1, 1
x2_min_norm, x2_max_norm = -1, 1


def averageY(y):
    average_Y = []
    for i in range(len(y)):
        sum = 0
        for j in y[i]:
            sum += j
        average_Y.append(sum / len(y[i]))
    return average_Y


def dispersion(y):
    disp = []
    for i in range(len(y)):
        sum = 0
        for j in y[i]:
            sum += (j - averageY(y)[i]) ** 2
        disp.append(sum / len(y[i]))
    return disp


def fuv(u, v):
    if u >= v:
        return u / v
    else:
        return v / u


def discriminant(x11, x12, x13, x21, x22, x23, x31, x32, x33):
    return x11 * x22 * x33 + x12 * x23 * x31 + x32 * x21 * x13 - x13 * x22 * x31 - x32 * x23 * x11 - x12 * x21 * x33


y = [[r.randint(y_min, y_max) for j in range(6)] for i in range(rows)]
average_Y = averageY(y)

# common dispersion
teta_sigma = math.sqrt((2 * (2 * m - 2)) / (m * (m - 4)))

Fuv = []
teta = []
Ruv = []

Fuv.append(fuv(dispersion(y)[0], dispersion(y)[1]))
Fuv.append(fuv(dispersion(y)[2], dispersion(y)[0]))
Fuv.append(fuv(dispersion(y)[2], dispersion(y)[1]))

teta.append(((m - 2) / m) * Fuv[0])
teta.append(((m - 2) / m) * Fuv[1])
teta.append(((m - 2) / m) * Fuv[2])

Ruv.append(abs(teta[0] - 1) / teta_sigma)
Ruv.append(abs(teta[1] - 1) / teta_sigma)
Ruv.append(abs(teta[2] - 1) / teta_sigma)

Rkr = 2  # koef for p = 0.9

for i in range(len(Ruv)):
    if Ruv[i] > Rkr:
        print('Помилка, повторіть експеримент')
        sys.exit()

mx1 = (-1 + 1 - 1) / 3
mx2 = (-1 - 1 + 1) / 3
my = sum(average_Y) / 3
a1 = (1 + 1 + 1) / 3
a2 = (1 - 1 - 1) / 3
a3 = (1 + 1 + 1) / 3
a11 = (-1 * average_Y[0] + 1 * average_Y[1] - 1 * average_Y[2]) / 3
a22 = (-1 * average_Y[0] - 1 * average_Y[1] + 1 * average_Y[2]) / 3

b0 = discriminant(my, mx1, mx2, a11, a1, a2, a22, a2, a3) / discriminant(1, mx1, mx2, mx1, a1, a2, mx2, a2, a3)
b1 = discriminant(1, my, mx2, mx1, a11, a2, mx2, a22, a3) / discriminant(1, mx1, mx2, mx1, a1, a2, mx2, a2, a3)
b2 = discriminant(1, mx1, my, mx1, a1, a11, mx2, a2, a22) / discriminant(1, mx1, mx2, mx1, a1, a2, mx2, a2, a3)

y_pr1 = b0 + b1 * x1_min_norm + b2 * x2_min_norm
y_pr2 = b0 + b1 * x1_max_norm + b2 * x2_min_norm
y_pr3 = b0 + b1 * x1_min_norm + b2 * x2_max_norm

dx1 = abs(x1_max - x1_min) / 2
dx2 = abs(x2_max - x2_min) / 2
x10 = (x1_max + x1_min) / 2
x20 = (x2_max + x2_min) / 2

koef0 = b0 - (b1 * x10 / dx1) - (b2 * x20 / dx2)
koef1 = b1 / dx1
koef2 = b2 / dx2

yP1 = koef0 + koef1 * x1_min + koef2 * x2_min
yP2 = koef0 + koef1 * x1_max + koef2 * x2_min
yP3 = koef0 + koef1 * x1_min + koef2 * x2_max

print('Матриця планування для m =', m)
for i in range(rows):
    print(y[i])
print('Експериментальні значення критерію Романовського:')
for i in range(rows):
    print(Ruv[i])

print('Натуралізовані коефіцієнти: \na0 =', round(koef0, 4), 'a1 =', round(koef1, 4), 'a2 =', round(koef2, 4))
print('У практичний ', round(y_pr1, 4), round(y_pr2, 4), round(y_pr3, 4),
      '\nУ середній', round(average_Y[0], 4), round(average_Y[1], 4), round(average_Y[2], 4))
print('У практичний норм.', round(yP1, 4), round(yP2, 4), round(yP3, 4))

