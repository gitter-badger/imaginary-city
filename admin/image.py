import os
import io
import PIL.Image


class ImageHandler:
    inst = None

    def __init__(self):
        ImageHandler.inst = self

    def listImage(self, filepath):
        return [fn for fn in os.listdir("../frontend/blog/" + filepath) 
                          if fn.endswith(".png") or fn.endswith(".jpg") or fn.endswith(".gif")]

    def uploadImage(self, filepath, filename, filebody):
        file_like = io.BytesIO(filebody)
        img = PIL.Image.open(file_like)
        file_with_path  = "../frontend/blog/" + filepath + "/" + filename
        print(file_with_path)
        img.save(file_with_path) 
