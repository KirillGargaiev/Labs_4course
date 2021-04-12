import random
import math


def x_list():
    temp = []
    for i in range(8):
        r = random.randint(1, 20)
        temp.append(r)
    return temp


a0 = 8
a1 = 5
a2 = 3
a3 = 9

x1 = x_list()
x2 = x_list()
x3 = x_list()


def calculate_y(x_1, x_2, x_3):
    return a0 + a1 * x_1 + a2 * x_2 + a3 * x_3


y = [calculate_y(x1[i], x2[i], x3[i]) for i in range(8)]

x01 = (max(x1) + min(x1)) / 2
x02 = (max(x2) + min(x2)) / 2
x03 = (max(x3) + min(x3)) / 2

dx1 = x01 - min(x1)
dx2 = x02 - min(x2)
dx3 = x03 - min(x3)

xn1 = [(x1[i] - x01) / dx1 for i in range(8)]
xn2 = [(x2[i] - x02) / dx2 for i in range(8)]
xn3 = [(x3[i] - x03) / dx3 for i in range(8)]

y_et = calculate_y(x01, x02, x03)
print(y)
print(y_et)
print(min(y))
