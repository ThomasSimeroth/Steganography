from PIL import Image
im = Image.open("example.jpg")
width, height = im.size
for i in range(width):
    for j in range(height):
        pixel = im.getpixel((i,j))
        print(pixel)

