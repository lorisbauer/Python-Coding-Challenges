import numpy as np

m = [
    [1, 0, 0],
    [1, 0, 1],
    [0, 1, 1],
    [0, 1, 0]
]
n = np.array(m)
print(np.linalg.matrix_rank(n))
