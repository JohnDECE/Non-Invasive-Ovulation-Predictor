from hmmlearn import hmm
from cluster import clusterMaker
from skimage.io import imread
import numpy as np
import os

class PredictorModel:
    def __init__(self, dataDir):
        self.data = self.loadData(dataDir)
        self.hmmodel = hmm.GaussianHMM(n_components=2, n_iter=1000)

    def loadData(self, dataDir):
        """
        Loads images from the directory: dataDir
        Images should be clustered, but can accept any directory with images
        TODO: Filter out bad images as best as possible
        :param dataDir:
        :return:
        """
        fileList = [file for file in os.listdir(dataDir) if clusterMaker.check_dir_filetype(dataDir, file)]
        return np.array([np.array(imread(os.path.join(dataDir, file))) for file in fileList])

    def train(self):
        self.hmmodel.fit(self.data)
        pass