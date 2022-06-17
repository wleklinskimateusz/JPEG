from matplotlib import pyplot as plt
import numpy as np
from skimage import img_as_float, io
from scipy import fft

from zigzag import get_zigzag_row_col

quantization = np.array(
    [
        [
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99],
        ]
    ]
)


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


class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ""


def printNodes(node, val=""):
    # huffman code for current node
    newVal = val + str(node.huff)

    # if node is not an edge node
    # then traverse inside it
    if node.left:
        printNodes(node.left, newVal)
    if node.right:
        printNodes(node.right, newVal)

        # if node is edge node then
        # display its huffman code
    if not node.left and not node.right:
        print(f"{node.symbol} -> {newVal}")


class HuffmanTree:
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value
        self.nodes = [left, right]

    def encode(self):
        while len(self.nodes) > 1:
            # sort all the nodes in ascending order
            # based on theri frequency
            nodes = sorted(self.nodes, key=lambda x: x.freq)

            # pick 2 smallest nodes
            left = nodes[0]
            right = nodes[1]

            # assign directional value to these nodes
            left.huff = 0
            right.huff = 1

            # combine the 2 smallest nodes to create
            # new node as their parent
            newNode = Node(
                left.freq + right.freq, left.symbol + right.symbol, left, right
            )

            # remove the 2 nodes and add their
            # parent as new node among others
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(newNode)
            self.nodes = nodes


class JPEGencoder:
    def __init__(self, matrix: np.ndarray) -> None:
        self.pixels = matrix
        self.splitted_pixels = []
        self.blocks = None

    def split_pixels(self) -> None:
        self.blocks = self.pixels.shape[0] // 8
        for i in range(self.blocks):
            for j in range(self.blocks):
                self.splitted_pixels.append(
                    self.pixels[8 * i : 8 * i + 8, 8 * j : 8 * j + 8]
                )

    def color_space_transform(self) -> None:
        for i in range(len(self.splitted_pixels)):
            self.splitted_pixels[i] = ycbcr(self.splitted_pixels[i])

    def apply_dct(self) -> None:
        for i in range(len(self.splitted_pixels)):
            self.splitted_pixels[i] = fft.dct(self.splitted_pixels[i])

    def quantization_transform(self) -> None:
        for i in range(len(self.splitted_pixels)):
            for c in range(3):
                self.splitted_pixels[i][:, :, c] = (
                    self.splitted_pixels[i][:, :, c] / quantization
                )

    def zigzag_block(self, block):
        """
        Apply ZigZag Scan on a block
        """
        output = []
        for c in range(3):
            for i in range(len(block) ** 2):
                row, col = get_zigzag_row_col(i)
                output.append(block[row, col, c])

        return output

    def zigzag(self):
        for i in range(len(self.splitted_pixels)):
            self.splitted_pixels[i] = self.zigzag_block(self.splitted_pixels[i])

    def dcpm(self):
        """
        Apply Differential Pulse Code Modulation on a block
        """
        output = []
        for i in range(len(self.splitted_pixels)):
            if i == 0:
                output.append(self.splitted_pixels[i])
                continue
            output.append(self.splitted_pixels[i] - self.splitted_pixels[i - 1])
        self.splitted_pixels = output

    def run(self):
        self.split_pixels()
        self.color_space_transform()
        self.apply_dct()
        self.quantization_transform()
        self.zigzag()
        # self.dcpm()


class JPEGDecoder:
    def __init__(self, segments: np.ndarray) -> None:
        self.segments = segments
        self.image = None

    def unquantization_transform(self) -> None:
        for i in range(len(self.segments)):
            for c in range(3):
                self.segments[i][:, :, c] = self.segments[i][:, :, c] * quantization

    def apply_idct(self) -> None:
        for i in range(len(self.segments)):
            self.segments[i] = fft.idct(self.segments[i])

    def color_space_transform(self) -> None:
        for i in range(len(self.segments)):
            self.segments[i] = rgb(self.segments[i])

    def merge_pixels(self) -> None:
        blocks = int(len(self.segments) ** 0.5 + 0.1)
        self.image = np.zeros((blocks * 8, blocks * 8, 3))
        for i in range(blocks):
            for j in range(blocks):
                self.image[8 * i : 8 * i + 8, 8 * j : 8 * j + 8] = self.segments[
                    blocks * i + j
                ]

    def unzigzag_block(self, block):
        """
        Apply ZigZag Scan on a block
        """
        output = np.zeros((8, 8, 3))
        a = len(block) // 3
        for c in range(3):
            for i in range(a):
                row, col = get_zigzag_row_col(i)
                output[row, col, c] = block[i + c * a]

        return output

    def unzigzag(self):
        for i in range(len(self.segments)):
            self.segments[i] = self.unzigzag_block(self.segments[i])

    def run(self):
        self.unzigzag()
        self.unquantization_transform()
        self.apply_idct()
        self.color_space_transform()
        self.merge_pixels()


# class JPEGDecoder:
#     def __init__(self, filename: str) -> None:
#         self.filename = filename
#         self.bits = None

#     def open_file(self) -> None:
#         try:
#             with open(self.filename, "rb") as f:
#                 self.bits = np.fromfile(f, np.dtype("B"))
#         except IOError:
#             print("Error While Opening the file!")

#     def unqu


m = img_as_float(io.imread("myjpg.jpg"))
jpeg = JPEGencoder(m)
jpeg.run()
result = JPEGDecoder(jpeg.splitted_pixels)
result.run()
plt.imshow(result.image)

plt.show()
