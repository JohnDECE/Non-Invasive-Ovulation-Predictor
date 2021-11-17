from sklearn.cluster import KMeans
import os
from tkinter import Tk, filedialog
import cv2

class clusterMaker:
    def __init__(self, directory):
        assert os.path.isdir(directory)
        self.directory = directory
        self.fileList = os.listdir(self.directory) # May need to check for other directories and check for file type
        print(self.fileList[0], self.directory)
    def cluster(self):
        path = "/".join([self.fileList[0],self.directory])

        img = cv2.imread(path)

        orig = img.copy()

        reshaped = img.flatten()

        kmeans = KMeans(n_clusters=2,n_init=40, max_iter=500).fit(reshaped)

        pass

def main():
    root = Tk()
    root.withdraw()

    root.attributes("-topmost", True)

    directory = filedialog.askdirectory()

    assert directory

    clusterer = clusterMaker(directory)
    print(clusterer.fileList)

main()

