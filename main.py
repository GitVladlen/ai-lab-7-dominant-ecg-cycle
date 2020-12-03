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
    # fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 6))
    # plt.subplots_adjust(wspace=0.2, hspace=0.4)
    p1.plot(x1, 'r')
    p1.set_title('1')
    p2.plot(x2, 'b')
    p2.set_title('2')
    p3.plot(x3, 'g')
    p3.set_title('3')
    p4.plot(x4, 'y')
    p4.set_title('4')
    # plt.show()


def plotting_dxdz(p5, p6, x1, t1, x2, t2, x3, t3, x4, t4):
    # fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))
    p5.plot(x1, t1, 'r')
    p5.plot(x2, t2, 'b')
    p5.plot(x3, t3, 'g')
    p5.plot(x4, t4, 'y')
    p5.set_title('Phases graphic')
    p6.plot(x1, t1, 'r', linewidth=9)
    p6.plot(x2, t2, 'b')
    p6.plot(x3, t3, 'g')
    p6.plot(x4, t4, 'y')
    p6.set_title('Phases graphic with dominant sequence')
    # plt.show()


def plot(p1, p2, p3, p4, p5, p6, x, norm_x, der_norm_x):
    plotting(
        p1, p2, p3, p4
        , x[0], x[1], x[2], x[3]
    )
    # plotting(x[0], x[1], x[2], x[3])
    plotting_dxdz(
        p5, p6,
        der_norm_x[0], norm_x[0],
        der_norm_x[1], norm_x[1],
        der_norm_x[2], norm_x[2],
        der_norm_x[3], norm_x[3]
    )


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
root.wm_title("Визначення опорного циклу ЕКГ")

fig = Figure(figsize=(10, 6), dpi=100)

fig.subplots_adjust(wspace=0, hspace=0.4)

sub_plot_1 = fig.add_subplot(321)
sub_plot_2 = fig.add_subplot(322)
sub_plot_3 = fig.add_subplot(323)
sub_plot_4 = fig.add_subplot(324)
sub_plot_5 = fig.add_subplot(325)
sub_plot_6 = fig.add_subplot(326)

# sub_plot_1.set_title('Original Signal')
# sub_plot_2.set_title('Phases on dz/dt')
# sub_plot_3.set_title('Phases on z(t - pause)')

plot(
    sub_plot_1, sub_plot_2,
    sub_plot_3, sub_plot_4,
    sub_plot_5, sub_plot_6,
    x, norm_x, der_norm_x
)

fig.subplots_adjust(wspace=0.2, hspace=0.4)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

R = np.zeros((4, 4))
for i in range(4):
    for j in range(4):
        R[i, j] = round(directed_hausdorff(norm_x[i], norm_x[j])[0], 3)

print('\n\nDistance Hausdorf:\n\n' + str(R) + '\n\n')
print(np.argmin(R.sum(axis=1)) + 1)

root.mainloop()


