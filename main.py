import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import directed_hausdorff


def read_from_file(file_name):
    f = open(file_name, 'r')
    lines = []
    for line in f:
        lines += line.split()
    signal = np.array(lines, dtype=np.float)
    return signal


def plotting(p1, p2, p3, p4, x1, x2, x3, x4):
    p1.plot(x1, 'r')
    p1.set_title('ЕКГ 1')

    p2.plot(x2, 'b')
    p2.set_title('ЕКГ 2')

    p3.plot(x3, 'g')
    p3.set_title('ЕКГ 3')

    p4.plot(x4, 'y')
    p4.set_title('ЕКГ 4')


def plotting_dxdz(p5, p6, x1, t1, x2, t2, x3, t3, x4, t4, dominant):
    p5.plot(x1, t1, 'r')
    p5.plot(x2, t2, 'b')
    p5.plot(x3, t3, 'g')
    p5.plot(x4, t4, 'y')
    p5.set_title('Фазові портрети')

    if dominant == 1:
        p6.plot(x1, t1, 'r', linewidth=9)
    else:
        p6.plot(x1, t1, 'r')

    if dominant == 2:
        p6.plot(x2, t2, 'b', linewidth=9)
    else:
        p6.plot(x2, t2, 'b')

    if dominant == 3:
        p6.plot(x3, t3, 'g', linewidth=9)
    else:
        p6.plot(x3, t3, 'g')

    if dominant == 4:
        p6.plot(x4, t4, 'y', linewidth=9)
    else:
        p6.plot(x4, t4, 'y')
    p6.set_title('З домінантим сигналом')


# def plot(p1, p2, p3, p4, p5, p6, x, norm_x, der_norm_x):
#     plotting(
#         p1, p2, p3, p4
#         , x[0], x[1], x[2], x[3]
#     )
#     # plotting(x[0], x[1], x[2], x[3])
#     plotting_dxdz(
#         p5, p6,
#         der_norm_x[0], norm_x[0],
#         der_norm_x[1], norm_x[1],
#         der_norm_x[2], norm_x[2],
#         der_norm_x[3], norm_x[3],
#         1
#     )


def derivat(x):
    z = []
    len_x = len(x)
    for i in range(len_x):
        a = x[i + 3] if i + 3 < len_x else x[-1]
        b = x[i + 2] if i + 2 < len_x else x[-1]
        c = x[i + 1] if i + 1 < len_x else x[-1]
        d = x[i - 1] if i - 1 >= 0 else x[0]
        e = x[i - 2] if i - 2 >= 0 else x[0]
        g = x[i - 3] if i - 3 >= 0 else x[0]
        z_i = (1/60) * (a -9*b +45*c -45*d +9*e -g)
        z.append(z_i)
    return np.array(z)


def normalize(x):
    z = ((x - min(x)) / (max(x) - min(x)))
    return z


x = np.array([read_from_file(str(i + 1) + '.txt') for i in range(4)])
norm_x = np.array([normalize(x[i]).reshape(len(x[i]), 1) for i in range(len(x))])
der_norm_x = np.array([normalize(derivat(x[i])) for i in range(len(x))])

import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tkinter.Tk()
# root.geometry("1200x300")
root.wm_title("Визначення опорного циклу ЕКГ")

R = np.zeros((4, 4))
for i in range(4):
    for j in range(4):
        R[i, j] = round(directed_hausdorff(norm_x[i], norm_x[j])[0], 3)

index = np.argmin(R.sum(axis=1)) + 1
text = '\n\nDistance Hausdorf:\n\n' + str(R) + '\n\n' + str(index)
print(text)

# Table
from prettytable import PrettyTable

table = PrettyTable()

table.field_names = ["Rij", "1", "2", "3", "4"]

for i, r in enumerate(R, 1):
    # row = []
    # row.append(str(i))
    # row += r
    a = [str(i)]
    for j, c in enumerate(r, 1):
        a.append(str(c))
    table.add_row(a)

tkinter.Label(root, text=str(table), font="Consolas 10").pack(side=tkinter.RIGHT)

# Fig 1
fig1 = Figure(figsize=(10, 3), dpi=100)

fig1.subplots_adjust(wspace=0, hspace=1)

sub_plot_1 = fig1.add_subplot(141)
sub_plot_2 = fig1.add_subplot(142)
sub_plot_3 = fig1.add_subplot(143)
sub_plot_4 = fig1.add_subplot(144)

plotting(
    sub_plot_1, sub_plot_2, sub_plot_3, sub_plot_4
    , x[0], x[1], x[2], x[3]
)

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.draw()

canvas1.get_tk_widget().pack(side=tkinter.TOP,
                             fill=tkinter.X,
                             # expand=1
                             )

# Fig 2
fig2 = Figure(figsize=(8, 4), dpi=100)

sub_plot_5 = fig2.add_subplot(121)
sub_plot_6 = fig2.add_subplot(122)

plotting_dxdz(
    sub_plot_5, sub_plot_6,
    der_norm_x[0], norm_x[0],
    der_norm_x[1], norm_x[1],
    der_norm_x[2], norm_x[2],
    der_norm_x[3], norm_x[3],
    index
)

fig2.subplots_adjust(wspace=0.5, hspace=1)

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.draw()

canvas2.get_tk_widget().pack(side=tkinter.BOTTOM,
                             fill=tkinter.X,
                             # expand=1
                             )

root.mainloop()


