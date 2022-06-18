import numpy as np


def ycbcr(image):
    A = np.array([0, 128, 128]).T
    matrix = np.array(
        [
            [0.299, 0.587, 0.114],
            [-0.168736, -0.331264, 0.5],
            [0.5, -0.418688, -0.081312],
        ]
    )
    return np.dot(image * 256, matrix) + A


def rgb(image):
    matrix = np.array(
        [
            [1, 0, 1.402],
            [1, -0.344136, -0.714136],
            [1, 1.772, 0],
        ]
    )
    return np.dot(image - np.array([0.0, 128.0, 128.0]).T, matrix) / 256


def get_zigzag_row_col(n):
    row = n // 8
    col = n % 8
    if row % 2 == 0:
        return row, col
    else:
        return row, 7 - col
