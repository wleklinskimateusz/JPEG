import numpy as np
from scipy import fft

from utils import get_zigzag_row_col, rgb
from const import quantization


class Decoder:
    """
    Class for decoding an image
    """

    def __init__(self, filename) -> None:
        """
        constructor for the decoder class
        """
        self.segments = None
        self.image = None
        self.filename = filename

    def load_file(self) -> None:
        """
        Load the file into the decoder
        """
        self.segments = np.load(self.filename).tolist()

    def undcpm(self):
        """
        Apply Differential Pulse Code Modulation on a block
        """
        for i in range(len(self.segments)):
            for j in range(1, len(self.segments[i])):
                self.segments[i][j] = self.segments[i][j] + self.segments[i][j - 1]

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
        """
        UnApply ZigZag Scan on the image
        """
        for i in range(len(self.segments)):
            self.segments[i] = self.unzigzag_block(self.segments[i])

    def unquantization_transform(self) -> None:
        """
        UnApply Quantization on a block
        """

        for i in range(len(self.segments)):
            for c in range(3):
                self.segments[i][:, :, c] = self.segments[i][:, :, c] / quantization

    def apply_idct(self) -> None:
        """
        Apply Inverse Discrete Cosine Transform on a block
        """
        for i in range(len(self.segments)):
            self.segments[i] = fft.idct(self.segments[i])

    def color_space_transform(self) -> None:
        """
        Returns the image to the original color space
        """

        for i in range(len(self.segments)):
            self.segments[i] = rgb(self.segments[i])

    def merge_pixels(self) -> None:
        """
        Merge the pixels into an image
        """
        blocks = int(len(self.segments) ** 0.5 + 0.1)
        self.image = np.zeros((blocks * 8, blocks * 8, 3))
        for i in range(blocks):
            for j in range(blocks):
                self.image[8 * i : 8 * i + 8, 8 * j : 8 * j + 8] = self.segments[
                    blocks * i + j
                ]

    def run(self):
        """
        Run the decoder
        """
        self.load_file()
        self.undcpm()
        self.unzigzag()
        self.unquantization_transform()
        self.apply_idct()
        self.color_space_transform()
        self.merge_pixels()
