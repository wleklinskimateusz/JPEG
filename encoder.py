import numpy as np

from utils import get_zigzag_row_col, ycbcr
from scipy import fft
from const import quantization


class Encoder:
    """
    A class for encoding an image
    """

    def __init__(self, matrix: np.ndarray, filename: str) -> None:
        """
        constructor for the encoder class
        """
        self.pixels = matrix
        self.splitted_pixels = []
        self.blocks = None
        self.filename = filename

    def split_pixels(self) -> None:
        """
        Split the image into blocks of 8x8 pixels
        """
        self.blocks = self.pixels.shape[0] // 8
        for i in range(self.blocks):
            for j in range(self.blocks):
                self.splitted_pixels.append(
                    self.pixels[8 * i : 8 * i + 8, 8 * j : 8 * j + 8]
                )

    def color_space_transform(self) -> None:
        """
        Transform the image to YCbCr color space
        """
        for i in range(len(self.splitted_pixels)):
            self.splitted_pixels[i] = ycbcr(self.splitted_pixels[i])

    def apply_dct(self) -> None:
        """
        Apply Discrete Cosine Transform on a block
        """
        for i in range(len(self.splitted_pixels)):
            self.splitted_pixels[i] = fft.dct(self.splitted_pixels[i])

    def quantization_transform(self) -> None:
        """
        Quantize the image
        """
        for i in range(len(self.splitted_pixels)):
            for c in range(3):
                self.splitted_pixels[i][:, :, c] = (
                    self.splitted_pixels[i][:, :, c] * quantization
                ).astype(int)

    def zigzag_block(self, block):
        """
        Apply ZigZag Scan on a block
        """
        output = []
        for c in range(3):
            for i in range(len(block) ** 2):
                row, col = get_zigzag_row_col(i)
                output.append(block[row, col, c])

        return np.array(output, dtype=int)

    def zigzag(self):
        """
        ZigZag Scan on the image
        """
        for i in range(len(self.splitted_pixels)):
            self.splitted_pixels[i] = self.zigzag_block(self.splitted_pixels[i])

    def dcpm(self):
        """
        Apply Differential Pulse Code Modulation on a block
        """
        for i in range(len(self.splitted_pixels)):
            output = np.zeros(len(self.splitted_pixels[i]), dtype=int)
            output[0] = self.splitted_pixels[i][0]
            for j in range(1, len(self.splitted_pixels[i])):
                output[j] = self.splitted_pixels[i][j] - self.splitted_pixels[i][j - 1]
            self.splitted_pixels[i] = output

    def save_to_binary(self) -> None:
        """
        Save the image to a binary file
        """
        np.save(self.filename, self.splitted_pixels)

    def run(self):
        """
        Run the encoder
        """
        self.split_pixels()
        self.color_space_transform()
        self.apply_dct()
        self.quantization_transform()
        self.zigzag()
        self.dcpm()
        self.save_to_binary()

        # print(self.splitted_pixels[50])
        # print(len(self.splitted_pixels))
