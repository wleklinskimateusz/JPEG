from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paint with PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Image
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        # Testing
        black_box = np.zeros((200, 50, 3), dtype=np.uint8) * 255
        self.load_image_from_matrix(black_box)

        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black

        # QPoint object to tract the point
        self.lastPoint = QPoint()

        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu("File")
        b_size = mainMenu.addMenu("Brush Size")
        b_color = mainMenu.addMenu("Brush Color")

        fileOptions = [
            {"name": "Save", "command": self.save},
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
        for i in range(min(self.image.width(), matrix.shape[0])):
            for j in range(min(self.image.height(), matrix.shape[1])):
                r, g, b = matrix[i, j]
                self.image.setPixelColor(i, j, QColor(r, g, b))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
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
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) "
        )

        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):

        self.image.fill(Qt.white)
        self.update()

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
