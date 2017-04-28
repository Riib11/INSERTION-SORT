from PIL import Image
from PIL import ImageDraw

def open_image(name):
    Image.open("assets/images/" + name).show()