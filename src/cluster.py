from sklearn.cluster import KMeans
import os
from tkinter import Tk, filedialog
from skimage.io import imread, imsave
import fileParser

class clusterMaker:
    def __init__(self, directory):
        assert os.path.isdir(directory) # Make sure that we actually received a directory, TODO: This may cause errors, may need to check then alert instead
        self.directory = directory
        # Below will store a list of all image file names in self.directory, we will exclude any other entries that are not images
        self.fileList = [file for file in os.listdir(self.directory) if fileParser.fileData.check_dir_filetype(directory, file)]
        # print(self.fileList[0], self.directory)

    def cluster(self, fileInd):
        """
        This function will perform k-means clustering on images.
        :return: Both the original image and clustered version as numpy arrays.
        """
        path = "/".join([self.directory, self.fileList[fileInd]])

        img = imread(path)

        reshaped = img.reshape(img.shape[0] * img.shape[1], img.shape[2])

        kmeans = KMeans(n_clusters=4, random_state=0).fit(reshaped)

        tempsum = kmeans.cluster_centers_.sum(axis=1)
        clusterind = tempsum.argmin() # Retrieve the index of the cluster with the lowest values (coldest pixels)

        clustered = kmeans.cluster_centers_[kmeans.labels_] #Retrieve the clustered image
        clustered = clustered.reshape((-1,3)) #reshape back into the H x W, Layers shape
        clustered[kmeans.labels_ == clusterind] = [0, 0, 0] # Filter out the cold pixels

        clustered_3D = clustered.reshape(img.shape).astype('uint8')
        # img = img.astype('uint8')

        #return img, clustered_3D
        return clustered_3D # return the clustered image with the cold pixels removed

    def cluster_directory_images(self):
        """
        This is a python generator for clustering images in self.directory.
        We will process each image in self.directory one by one and each time an image is clustered we yield it like
        a python generator
        :return: a generator containing the clustered image
        """
        for fileInd in range(len(self.fileList)):
            yield self.cluster(fileInd)

    def save_images_to_directory(self, imgList, directory=None):
        """
        Save the images in imgList as files in directory. If directory is none, then create a default output directory
        in the directory saved at self.directory
        :param directory: Defaults to none, a directory to save the images in, must be absolute path
        :return: The directory that the images were saved at
        """
        outdir = "output"
        if directory is not None:
            outdir = directory

        DirPath = "/".join([self.directory, outdir])
        if not os.path.exists(DirPath):
            os.makedirs(DirPath)

        for ind, img in enumerate(imgList):
            fileName = "_".join(["clustered", self.fileList[ind]])
            imsave(os.path.join(DirPath, fileName), img)
        return DirPath

def main():
    root = Tk()
    root.withdraw()

    root.attributes("-topmost", True)

    directory = filedialog.askdirectory()

    assert directory

    clusterer = clusterMaker(directory)
    print(clusterer.fileList)
    #originalimage, clusteredimg = clusterer.cluster()

    print(clusterer.save_images_to_directory(clusterer.cluster_directory_images()))

if __name__ == "__main__":
    main()