from PIL import Image
im = Image.open("example.jpg")
print(im.format, im.size, im.mode)