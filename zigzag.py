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
