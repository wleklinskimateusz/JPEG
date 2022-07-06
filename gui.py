from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np

from encoder import Encoder
from decoder import Decoder


class Window(QMainWindow):
    """
    Main Window For GUI
    """

    def __init__(self):
        """
        The constructor for the main window.
        """
        super().__init__()
        self.setWindowTitle("JPEG GUI")  # Set the title of the window.
        self.setGeometry(64, 64, 512, 512)  # Set the size and position of the window.

        # Image
        self.image = QImage(self.size(), QImage.Format_RGB32)  # Create the image.
        self.image.fill(Qt.white)  # Fill the image with white.

        # Initialize the brush size and color.
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black

        # QPoint object to tract the point
        self.lastPoint = QPoint()

        # Create the menu bar.
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu("File")
        b_size = mainMenu.addMenu("Brush Size")
        b_color = mainMenu.addMenu("Brush Color")

        fileOptions = [
            {"name": "Save", "command": self.save},
            {"name": "Load", "command": self.load},
            {"name": "Clear", "command": self.clear},
        ]
        for fileOption in fileOptions:
            self.save_menu_action(**fileOption, menu=fileMenu)

        sizes = [
            {"name": "4px", "action": self.Pixel_4},
            {"name": "7px", "action": self.Pixel_7},
            {"name": "9px", "action": self.Pixel_9},
            {"name": "12px", "action": self.Pixel_12},
        ]
        for size in sizes:
            self.save_menu_action(size["name"], size["action"], b_size)

        colors = [
            {"name": "Black", "color": self.blackColor},
            {"name": "White", "color": self.whiteColor},
            {"name": "Green", "color": self.greenColor},
            {"name": "Yellow", "color": self.yellowColor},
            {"name": "Red", "color": self.redColor},
        ]

        for color in colors:
            self.save_menu_action(color["name"], color["color"], b_color)

    def save_menu_action(self, name: str, command, menu: QMenu):
        """
        Creates a menu action and adds it to the menu.
        params:
            name: The name of the menu action.
            command: The command to execute when the menu action is clicked.
            menu: The menu to add the menu action to.

        """
        action = QAction(name, self)
        action.triggered.connect(command)
        menu.addAction(action)

    def load_image_from_matrix(self, matrix: np.ndarray):
        """
        Loads an image from a matrix.
        :param matrix: The matrix to load the image from.
        :return: None.

        matrix must be NxMx3. (width, height, color ~ 0-255)
        """
        for i in range(min(self.image.width(), matrix.shape[1])):
            for j in range(min(self.image.height(), matrix.shape[0])):
                r, g, b = matrix[j, i]
                self.image.setPixelColor(i, j, QColor(r, g, b))
        self.update()

    def save_image_to_matrix(self) -> np.ndarray:
        """
        Saves the image to a matrix.
        :return: The image as a matrix.
        """
        matrix = np.zeros((self.image.height(), self.image.width(), 3), dtype=np.uint8)
        for i in range(self.image.width()):
            for j in range(self.image.height()):
                matrix[j, i] = self.image.pixel(i, j)
        return matrix

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        handles the mouse press event.
        """
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        handles the mouse move event.
        """
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.brushSize,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Handles the mouse release event.
        """
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        """
        Handles the paint event.
        """

        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        """
        saves the image to a .npy file.
        """

        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Images (*.npy)"
        )

        if filePath == "":
            return
        jpeg = Encoder(self.save_image_to_matrix(), filePath)
        jpeg.run()

    def clear(self):
        """
        Clears the image.
        """

        self.image.fill(Qt.white)
        self.update()

    def load(self):
        """
        Loads an image from a .npy file.
        """
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Load Image", "", "Image Files (*.npy)"
        )

        if filePath == "":
            return
        decoder = Decoder(filePath)
        decoder.run()
        self.load_image_from_matrix(decoder.image.astype(int))

        # Helper Functions to set the brush size and color.

    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

    def blackColor(self):
        self.brushColor = Qt.black

    def whiteColor(self):
        self.brushColor = Qt.white

    def greenColor(self):
        self.brushColor = Qt.green

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def redColor(self):
        self.brushColor = Qt.red
