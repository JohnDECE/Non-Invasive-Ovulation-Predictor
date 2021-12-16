import os
from PIL import Image

path = 'Pictures/'


def calculateTotal(image):
    im = Image.open(image)
    totalPixel = 0
    for xpixel in range(im.size[0]):
        for ypixel in range(im.size[1]):
            pixel = im.getpixel((xpixel, ypixel))
            totalPixel = totalPixel + pixel[0] + pixel[1] + pixel[2]
    print(totalPixel)
    return totalPixel



entries = os.scandir(path)
for files in entries:
    total = calculateTotal(path + files.name)
    if total > 7000000:
        os.remove(files.path)
        print("Image has been deleted")

