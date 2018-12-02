from PIL import Image

def encodeBit(value, bit):
    if value % 2 == 1 and bit % 2 == 0:
        return value - 1
    elif value % 2 == 0 and bit % 2 == 1:
        return value + 1
    else:
        return value

def encodeMessage(path, message):
    im = Image.open(path)
    width, height = im.size
    newImage = im.copy()
    pixels = newImage.load()
    #Needs to encrypt message
    byteString = ''.join(format(ord(x), 'b').zfill(8) for x in message)
    messageSize = len(byteString)
    if height < messageSize or width < messageSize:
        print("Message too big to encode")
        return None
    else:
        for i in range(len(byteString)):
            red, green, blue = im.getpixel((i,i))
            red = encodeBit(red, int(byteString[i]))
            #Only changes red value currently
            pixels[i, i] = (red, green, blue)
        newImage.save("example2.jpg", "png")
        return newImage
