from sklearn.cluster import KMeans
import os
from tkinter import Tk, filedialog
from skimage.io import imread
import matplotlib.pyplot as plt

class clusterMaker:
    def __init__(self, directory):
        assert os.path.isdir(directory)
        self.directory = directory
        self.fileList = os.listdir(self.directory) # May need to check for other directories and check for file type
        # print(self.fileList[0], self.directory)

    def cluster(self):
        """
        This function will perform k-means clustering on images.
        :return: Both the original image and clustered version as numpy arrays.
        """
        path = "/".join([self.directory, self.fileList[0]])

        img = imread(path)

        reshaped = img.reshape(img.shape[0] * img.shape[1], img.shape[2])

        kmeans = KMeans(n_clusters=5, random_state=0).fit(reshaped)

        clustered = kmeans.cluster_centers_[kmeans.labels_]

        clustered_3D = clustered.reshape(img.shape[0], img.shape[1], img.shape[2])

        return img, clustered_3D

def main():
    root = Tk()
    root.withdraw()

    root.attributes("-topmost", True)

    directory = filedialog.askdirectory()

    assert directory

    clusterer = clusterMaker(directory)
    print(clusterer.fileList)
    originalimage, clusteredimg = clusterer.cluster()

    plt.figure()
    plt.imshow(originalimage.astype('uint8'))
    plt.title('original')

    plt.figure()
    plt.imshow(clusteredimg.astype('uint8'))
    # plt.title("clustered")
    plt.axis('off')
    plt.savefig("test.png", bbox_inches='tight', pad_inches=0)
    plt.show()


main()

