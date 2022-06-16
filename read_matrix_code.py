from posixpath import split
import numpy as np


def hex_to_rgb(hex):
    print(hex)
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i : i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)


def decodeMatrix(n, m):
    data = []
    f = open("matrix_code.txt", "r")
    for x in f:
        data.append(x.split(","))
    f.close()

    data = np.array(data)
    matrix = np.zeros([3, n, m])

    n = int(n / 2)
    m = int(m / 2)

    hex = data.T[4]
    matrix_hex = np.reshape(hex, (n, m))

    for i in range(0, n - 1):
        for j in range(0, m - 1):
            k = i * 2
            l = j * 2
            matrix[0, k, l] = int(matrix_hex[i, j][1:3], 16)
            matrix[0, k + 1, l] = int(matrix_hex[i + 1, j][1:3], 16)
            matrix[0, k, l + 1] = int(matrix_hex[i, j + 1][1:3], 16)
            matrix[0, k + 1, l + 1] = int(matrix_hex[i + 1, j + 1][1:3], 16)

            matrix[1, k, l] = int(matrix_hex[i, j][3:5], 16)
            matrix[1, k + 1, l] = int(matrix_hex[i + 1, j][3:5], 16)
            matrix[1, k, l + 1] = int(matrix_hex[i, j + 1][3:5], 16)
            matrix[1, k + 1, l + 1] = int(matrix_hex[i + 1, j + 1][3:5], 16)

            matrix[2, k, l] = int(matrix_hex[i, j][5:7], 16)
            matrix[2, k + 1, l] = int(matrix_hex[i + 1, j][5:7], 16)
            matrix[2, k, l + 1] = int(matrix_hex[i, j + 1][5:7], 16)
            matrix[2, k + 1, l + 1] = int(matrix_hex[i + 1, j + 1][5:7], 16)

    matrix = matrix[:, :-2, :-2]

    return matrix
