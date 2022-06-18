from matplotlib import pyplot as plt
from gui import Window, QApplication
import sys
from skimage import img_as_float, io

from encoder import Encoder
from decoder import Decoder


def main():
    m = img_as_float(io.imread("myjpg.jpg"))
    jpeg = Encoder(m)
    jpeg.run()
    result = Decoder(jpeg.splitted_pixels)
    result.run()
    plt.imshow(result.image)
    plt.show()
    # App = QApplication(sys.argv)
    # window = Window()
    # window.show()
    # sys.exit(App.exec_())


if __name__ == "__main__":
    main()
