import numpy as np
from numba import jit
import matplotlib.pyplot as plt


@jit(nopython=True)
def mandelbrot(re, im, max_iter):
    c = complex(re, im)
    z = 0.0j

    for i in range(max_iter):
        z = z ** 2 + c
        if abs(z) >= 2:
            return i
    return max_iter


x_range, y_range = (-2, 1), (-1, 1)
# rows = cols = 2000
# result = np.zeros([rows, cols])
#
# for i, re in enumerate(np.linspace(*x_range, rows)):
#     for j, im in enumerate(np.linspace(*y_range, cols)):
#         result[i][j] = mandelbrot(re, im, 400)
#
# with open('MandelBrot.npy', 'wb') as f:
#     np.save(f, result.T)

with open('MandelBrot.npy', 'rb') as f:
     result = np.load(f)

plt.imshow(result, cmap='hot', interpolation='bicubic', extent=[*x_range, *y_range])
plt.show()
