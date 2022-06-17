# import numpy as np


# class Space:
#     def __init__(self, row, col):
#         self.row = row
#         self.col = col

#     def __repr__(self):
#         return f"{self.row} {self.col}"


# class Zigzag:
#     def __init__(self, block: np.ndarray) -> None:
#         self.block = block
#         self.previous_space = Space(0, 0)

#     def next_space(self, space: Space) -> Space:
#         if space.row == self.previous_space.row == -7:
#             return Space(space.row + 1, space.col + 1)

#         if space.row == -7:
#             return Space(space.row, space.col + 1)

#         if space.col == -7 and space.row == 0:
#             return Space(space.row + 1, space.col-1)


#         if space.row == 0 and space.col == 0:
#             return Space(0, 1)
#         if space.row == 0 and self.previous_space.row == 0:
#             return Space(1, space.col - 1)
#         if space.row == 0:
#             return Space(0, space.col + 1)

#         if space.col == self.previous_space.col == 0:
#             return Space(space.row + 1, space.col + 1)

#         if space.col == 0:
#             return Space(space.row + 1, 0)

#     def run(self):
#         output = []
#         for color in range(3):
#             space = Space(0, 0)
#             while space.x != 7 and space.y != 7:
#                 output.append(self.block[space.x, space.y, color])
#                 self.previous_space = space
#                 space = self.next_space(space)

import numpy as np


idx = np.array(
    [
        [0, 1, 5, 6, 14, 15, 27, 28],
        [2, 4, 7, 13, 16, 26, 29, 42],
        [3, 8, 12, 17, 25, 30, 41, 43],
        [9, 11, 18, 24, 31, 40, 44, 53],
        [10, 19, 23, 32, 39, 45, 52, 54],
        [20, 22, 33, 38, 46, 51, 55, 60],
        [21, 34, 37, 47, 50, 56, 59, 61],
        [35, 36, 48, 49, 57, 58, 62, 63],
    ]
)


def get_zigzag_row_col(n):
    row = n // 8
    col = n % 8
    if row % 2 == 0:
        return row, col
    else:
        return row, 7 - col


def get_zigzag_idx(row, col):
    return idx[row, col]


output = np.zeros((8, 8))
for i in range(8):
    for j in range(8):
        row, col = get_zigzag_row_col(idx[i, j])
        output[row, col] = idx[i, j]
print(output)
result = np.zeros((8, 8))
for i in range(8):
    for j in range(8):
        result[i, j] = get_zigzag_idx(i, j)
print(result)
