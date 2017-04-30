import os

class ImageHandler:
    inst = None

    def __init__(self):
        ImageHandler.inst = self

    def listImage(self, filepath):
        return [fn for fn in os.listdir("../frontend/blog/" + filepath) if fn.endswith(".png")]
