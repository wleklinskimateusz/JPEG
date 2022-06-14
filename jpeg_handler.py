import numpy as np
from PIL import Image


class JPEG:
    def __init__(self):
        pass

    def save(self, image: np.ndarray, file_path: str):

        im = Image.fromarray(image)
        if not file_path.endswith(".jpg"):
            file_path += ".jpg"
        im.save(file_path, "JPEG")

    def load(self, file_path: str):
        im = Image.open(file_path)
        return np.array(im)
