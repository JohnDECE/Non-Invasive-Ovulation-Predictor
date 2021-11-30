import os
import imghdr
from datetime import datetime

class fileData:
    def __init__(self, directory, fileName):
        """
        This will initialize a file data object given a directory and file name.

        The resultant object will have 4 attributes:
        self.directory
        self.fileName
        self.fileNum
        self.datetime

        The first 2 are self explanatory, they contain the directory that holds the file and the file's name

        The third attribute contains the file's number or in other words it tells us how many files have been created before it including itself
        Thus if self.fileNum = 100, then it is the 100th recorded file since the start of recording. This may be useful in understanding the time sequence of files

        self.datetime contains a datetime python object from the datetime module, which has the date
        :param directory: a string containing the absolute path to the directory containing our files
        :param fileName: the file's name
        """
        assert self.check_dir_filetype(directory, fileName)
        self.directory = directory
        self.fileName = fileName
        self.__parseFileName()

    def __parseFileName(self):
        """
        This private method will parse a filename as given by the image files that were setup by Will.
        It will initialize the fileNum and datetime attributes.
        :return: Nothing
        """
        fileNameParts = self.fileName.split(".")[0].split("_") # remove file extension then extract all parts of the file name
        fileNumber = fileNameParts[0]
        day = int(fileNameParts[1])
        month = int(fileNameParts[2])
        year = int(fileNameParts[3])
        hour = int(fileNameParts[4])
        minute = int(fileNameParts[5])
        second = int(fileNameParts[6])

        self.fileNum = int(fileNumber)
        self.datetime = datetime(year=year,month=month, day=day,hour=hour, minute=minute, second=second)

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