import numpy as np


def decodeMatrix(n, m):
    data = []
    f = open("matrix_code.txt", "r")
    for x in f:
        data.append(x.split(","))
    f.close()

    data = np.array(data)
    matrix = np.zeros([n, m, 3])

    hex = data.T[4]
    matrix_hex = np.reshape(hex, (n, m))
    n = n // 2
    m = m // 2

    for i in range(0, n - 1):
        for j in range(0, m - 1):
            k = i * 2
            l = j * 2
            matrix[k, l, 0] = int(matrix_hex[i, j][1:3], 16)
            matrix[k + 1, l, 0] = int(matrix_hex[i + 1, j][1:3], 16)
            matrix[k, l + 1, 0] = int(matrix_hex[i, j + 1][1:3], 16)
            matrix[k + 1, l + 1, 0] = int(matrix_hex[i + 1, j + 1][1:3], 16)

            matrix[k, l, 1] = int(matrix_hex[i, j][3:5], 16)
            matrix[k + 1, l, 1] = int(matrix_hex[i + 1, j][3:5], 16)
            matrix[k, l + 1, 1] = int(matrix_hex[i, j + 1][3:5], 16)
            matrix[k + 1, l + 1, 1] = int(matrix_hex[i + 1, j + 1][3:5], 16)

            matrix[k, l, 2] = int(matrix_hex[i, j][5:7], 16)
            matrix[k + 1, l, 2] = int(matrix_hex[i + 1, j][5:7], 16)
            matrix[k, l + 1, 2] = int(matrix_hex[i, j + 1][5:7], 16)
            matrix[k + 1, l + 1, 2] = int(matrix_hex[i + 1, j + 1][5:7], 16)

    matrix = matrix[:, :-2, :-2]

    return matrix
