import os
import imghdr
from datetime import datetime, date
from tkinter import Tk, filedialog

def sortKey(fileObj):
    """
    A helper function that helps with sorting our image files.
    Assuming the images were recorded using the recorder scripts then the first value after "clustered" (if it is a part of the file name)
    will indicate the order in which the files were recorded in, thus we sort by that value in ascending order.
    :param fileObj: A FileData Object
    :return: That value in the file name as an integer type
    """
    nameList = fileObj.fileName.split("_")
    if nameList[0] == "clustered":
        return int(nameList[1])
    else:
        return int(nameList[0])

class directoryData:
    def __init__(self, directory, hasTime):
        """
        This object will represent an entire directory.
        It will contain 2 attributes:
        self.directory - Contains directory absolute path
        self.fileObjs - Contains a list of fileData objects all of which represent individual image files
        :param directory: a string containing the absolute path to a directory
        """
        self.directory = directory
        # The list of file objects should be in the order that they came in via the dataset.
        # This is done by sorting via their file modification time
        self.fileObjs = [fileData(file, hasTime) for file in os.listdir(self.directory) if fileData.check_dir_filetype(self.directory, file)]
        self.fileObjs.sort(key=sortKey)

    def seperateFilesByDate(self):
        """
        This method will separate a directory of thermal image files by their date of recording.
        This method assumes that the files were recorded using the recorder scripts in the Non-Invasive-Ovulation Predictor Repo
        Therefore the file names of these images would contain timestamps/dates in the file names.

        :return: A dictionary with {Key:Value} Pairs of {Date string: List of images recorded for this date}
        """
        finalDict = {}
        tempList = []
        currentTime = None
        for file in self.fileObjs:
            fileName = file.fileName
            if type(file.datetime) == date:
                tempDate = file.datetime
            else:
                tempDate = file.datetime.date()
            if currentTime is None:
                currentTime = tempDate
                tempList.append(fileName)
            elif currentTime == tempDate:
                tempList.append(fileName)
            else:
                finalDict[currentTime.__str__()] = tempList.copy()
                tempList = []
                currentTime = tempDate
                tempList.append(fileName)
        return finalDict

class fileData:
    def __init__(self, fileName, hasTime):
        """
        This will initialize a file data object given a directory and file name.

        The resultant object will have 3 attributes:
        self.fileName
        self.fileNum
        self.datetime

        The first 1 is self explanatory, it contains the file's name

        The third attribute contains the file's number or in other words it tells us how many files have been created before it including itself
        Thus if self.fileNum = 100, then it is the 100th recorded file since the start of recording. This may be useful in understanding the time sequence of files

        self.datetime contains a datetime python object from the datetime module, which has the date
        :param fileName: the file's name
        """

        self.fileName = fileName
        self.hasTime = hasTime
        if self.hasTime:
            self.__parseFileName()
        else:
            self.__parseFileName_noTime()

    def __parseFileName(self):
        """
        This private method will parse a filename as given by the image files that were setup by Will.
        It will initialize the fileNum and datetime attributes.
        :return: Nothing
        """
        fileNameParts = self.fileName.split(".")[0].split("_") # remove file extension then extract all parts of the file name
        if fileNameParts[0] == "clustered":
            fileNameParts.pop(0)
        assert len(fileNameParts) <= 7
        fileNumber = fileNameParts[0]
        day = int(fileNameParts[1])
        month = int(fileNameParts[2])
        year = int(fileNameParts[3])
        hour = int(fileNameParts[4])
        minute = int(fileNameParts[5])
        second = int(fileNameParts[6])

        self.fileNum = int(fileNumber)
        self.datetime = datetime(year=year,month=month, day=day,hour=hour, minute=minute, second=second)

    def __parseFileName_noTime(self):
        """
        Same thing as the above private method, except for when the file name does not contain time stamps along side with the date
        :return: Nothing
        """
        fileNameParts = self.fileName.split(".")[0].split("_") # remove file extension then extract all parts of the file name
        if fileNameParts[0] == "clustered":
            fileNameParts.pop(0)
        assert len(fileNameParts) <= 5
        dayCount = fileNameParts[0]
        day = int(fileNameParts[1])
        month = int(fileNameParts[2])
        year = int(fileNameParts[3])

        self.fileNum = int(dayCount)
        self.datetime = date(year=year,month=month, day=day)

    @staticmethod
    def check_dir_filetype(directory, fileName):
        """
        Checks if the current file is a directory or is an image file type
        returns true only if the file is an image file
        :param directory:
        :param fileName:
        :return: True/False depending on if file is an image file
        """
        path = "/".join([directory, fileName])
        if os.path.isdir(path):  # filename is a directory
            return False
        elif imghdr.what(path) is None:  # filename is not an image and is not a directory
            return False
        else:  # Filename is an image file
            return True

    def __str__(self):
        return f"{self.fileName}, {self.fileNum}, {self.datetime}"

def askDir():
    """
    Simply opens up a file dialog and returns the selected directory
    :return: Absolute path of the selected directory as a string
    """
    root = Tk()
    root.withdraw()

    dir = filedialog.askdirectory()
    assert os.path.isdir(dir)
    return dir

def main():
    hasTime = False
    dir = askDir()
    timeCheck = input("Does the file name have the time in it (hours, minutes, seconds)? [y/n] Default is n: ")
    if timeCheck == "y":
        hasTime = True

    directoryObj = directoryData(dir, hasTime)
    print(directoryObj.fileObjs[0])
    blah = directoryObj.seperateFilesByDate()
    print()
if __name__ in "__main__":
    main()
