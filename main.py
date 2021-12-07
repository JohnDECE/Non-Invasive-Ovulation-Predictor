import os
from datetime import datetime

directory = "Pictures/"


def changeFileName():
    count = 0
    entries = os.scandir(directory)
    for files in entries:
        count = count + 1

    now = datetime.now()

    dt_string = now.strftime("_%d_%m_%Y_%H_%M_%S")
    file = "output.png"
    oldPath = file
    newPath = directory + str(count+1) + dt_string + '.png'
    os.rename(oldPath, newPath)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    changeFileName()
