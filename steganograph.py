from PIL import Image

def encodeMessage(path, message):
    im = Image.open(path)
    width, height = im.size
    newImage = im.copy()
    pixels = newImage.load()
    byteString = ''.join(format(ord(x), 'b') for x in message)
    messageSize = len(byteString)
    if height < messageSize or width < messageSize:
        return None
    else:
        for i in range(len(byteString)):
            red, green, blue = im.getpixel((i,i))
            red += int(byteString[i])
            pixels[i, i] = (red, green, blue)
        newImage.save("example2.jpg", "png")
        return newImage

encodeMessage("example.jpg", "Hello!")