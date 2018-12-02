from PIL import Image
im = Image.open("example.jpg")
width, height = im.size
st = "Hello!"
print(' '.join(format(ord(x), 'b') for x in st))
for i in range(width):
    for j in range(height):
        pixel = im.getpixel((i,j))
        #print(pixel)