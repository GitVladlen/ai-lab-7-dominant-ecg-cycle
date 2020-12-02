import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import directed_hausdorff
from scipy.spatial import distance_matrix


def read_from_file(file_name):
    f = open(file_name, 'r')
    arr = []
    for line in f:
        line_arr = line.split()
        arr += line_arr
    signal = np.array(arr, dtype=np.float)
    return signal


def plotting(x1, x2, x3, x4):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 6))
    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    ax1.plot(x1, 'r')
    ax1.set_title('1')
    ax2.plot(x2, 'r')
    ax2.set_title('2')
    ax3.plot(x3, 'r')
    ax3.set_title('3')
    ax4.plot(x4, 'r')
    ax4.set_title('4')
    plt.show()


def plotting_dxdz(x1, t1, x2, t2, x3, t3, x4, t4):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))
    ax1.plot(x1, t1, 'r')
    ax1.plot(x2, t2, 'b')
    ax1.plot(x3, t3, 'g')
    ax1.plot(x4, t4, 'y')
    ax1.set_title('Fhases graphic')
    ax2.plot(x1, t1, 'r', linewidth=9)
    ax2.plot(x2, t2, 'b')
    ax2.plot(x3, t3, 'g')
    ax2.plot(x4, t4, 'y')
    ax2.set_title('Fhases graphic with dominant sequence')
    plt.show()


def derivat(x):
    z = np.zeros((len(x)))
    for i in range(3, (len(x) - 3)):
        z[i] = (1 / 60) * (x[i - 3] - 9 * x[i + 2] + 45 * x[i + 1] - 45 * x[i - 1] + 9 * x[i - 2] - x[i - 3])
    return z


def normalize(x):
    z = None
    try:
        z = (x - np.min(x)) / (np.max(x) - np.min(x))
    except ValueError:
        pass

    return z


arr = []
for i in range(4):
    file_data = read_from_file(str(i + 1) + '.txt')
    arr.append(file_data)

x = np.array(arr)

norm_x_arr = []
for i in range(len(x)):
    norm = normalize(x[i])
    norm_x_arr.append(norm)

norm_x = np.array(norm_x_arr)

der_norm_x = np.array([normalize(derivat(x[i])) for i in range(len(x))])

plotting(x[0], x[1], x[2], x[3])
R = np.zeros((4, 4))
for i in range(4):
    for j in range(4):
        R[i, j] = round(directed_hausdorff(norm_x[i], norm_x[j])[0], 3)

print('\n\nDistance Hausdorf:\n\n' + str(R) + '\n\n')
print(np.argmin(R.sum(axis=1)) + 1)
plotting_dxdz(der_norm_x[0], norm_x[0], der_norm_x[1], norm_x[1], der_norm_x[2], norm_x[2], der_norm_x[3], norm_x[3])
