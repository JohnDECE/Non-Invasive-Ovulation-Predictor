from hmmlearn import hmm
from fileParser import fileData, directoryData, askDir
from skimage.io import imread
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pickle
import os
from datetime import date, timedelta
from tkinter import Tk, filedialog, simpledialog

class PredictorModel:
    def __init__(self, dataDir, hasTime, loadModel=None):
        """
        Initialize our modeller
        :param dataDir: An absolute path for the directory with the data we intend to use for training and prediction
        :param hasTime: Boolean for whether or not the image files have a timestamp alongside the date in the filename
        """
        self.dates, self.data = self.__loadData(dataDir, hasTime)
        if len(self.data.shape) == 1:
            self.workData = self.data.reshape(-1, 1)
        else:
            self.workData = self.data
        # print(self.data.shape, self.dates)
        self.dataDir = dataDir
        if loadModel:
            self.loadedModel = True
            self.loadModel(loadModel)
        else:
            self.loadedModel = False
            self.model = None

    def __loadData(self, dataDir, hasTime):
        """
        Loads images from the directory: dataDir
        Images should be clustered, but can accept any directory with images
        :param dataDir:
        :return: Numpy Array of the data with some processing
        """
        directoryObj = directoryData(dataDir, hasTime)
        fileDict = directoryObj.seperateFilesByDate()
        # Goal: Generate a numpy array of sequences, the sequences are made up of images from a single day
        # Process: Create
        finalList = []
        for fileList in fileDict.values():
            # Generate our sequence of images for a day
            tempList = []
            for file in fileList:
                tempList.append(imread(os.path.join(dataDir, file)))
            finalList.append(tempList)
        dateList = [date for date in fileDict.keys()]

        dateSeqList, seqList = self.__group_dates_into_seq(dateList, finalList, hasTime)
        finalArray = np.concatenate(tuple(seqList))

        return dateSeqList, finalArray

    def __group_dates_into_seq(self, dateList, dayImgList, hasTime):
        """
        Organizes the images in dayImgList into a nested list of lists of images that occurred in consecutive days
        Thus any images that suddenly appear on a day that is not consecutive will be a part of a different list

        Shape of final list:
        Top Layer: Lists representing sequences of consecutive days worth of images
        Next Layer: Lists representing a day's worth of images
        Last Layer: Images themselves

        :param dateList: A list of date strings that should be in chronological order
        :param dayImgList: A list of images in chronological order
        :param hasTime: A boolean representing whether the image file names have the timestamps in them
        :return: a final nested list with lists of lists of images that occurred in consecutive days
        """
        finalList = []
        finalDateList = []

        currentDate = None

        tempList = []
        tempDateList = []
        for index, item in enumerate(dateList):
            strList = item.split('-')
            tempDate = date(year=int(strList[0]), month=int(strList[1]), day=int(strList[2]))
            if currentDate is None:
                currentDate = tempDate
                tempList.append(np.mean(dayImgList[index]))
                tempDateList.append(item)
            elif currentDate + timedelta(days=1) == tempDate:
                currentDate = tempDate
                tempList.append(np.mean(dayImgList[index]))
                tempDateList.append(item)
            else:
                currentDate = tempDate
                finalList.append(tempList)
                finalDateList.append(tempDateList)
                tempList = []
                tempDateList = []
                tempList.append(np.mean(dayImgList[index]))
                tempDateList.append(item)
        finalList.append(tempList)
        finalDateList.append(tempDateList)
        return finalDateList, finalList

    def train(self):
        """
        Simply trains a Hidden Markov Model with Gaussian Emissions, 2 hidden states and 1000 iterations for the
        Baum-Welch Algorithm
        We will save the trained model into self.model.
        If we loaded in a model or already trained one, we will raise an error.
        :return: Nothing
        """
        assert self.model is None
        self.model = hmm.GaussianHMM(n_components=2, n_iter=1000).fit(self.workData, [len(seq) for seq in self.dates])

    def predict(self, sampleNum):
        """
        Tries to predict what the hidden states are using our trained model on our data set.

        This will automatically reorganize our hidden states such that state 0 = Non-Ovulation and State 1 = Ovulation.
        :param sampleNum: Total number of samples to create when hmmlearn's sample function is called.
               (Currently has no use, just left it in in case it does need to be used)
        :return: All relevant values that are associated with the model's prediction.
        """
        assert self.model
        mus, sigmas, P, hidden_states = self.__reorganize_states(self.model.predict(self.workData, [len(seq) for seq in self.dates]))
        logprob = self.model.score(self.workData, [len(seq) for seq in self.dates])
        samples = self.model.sample(sampleNum)
        return mus, sigmas, P, logprob, samples, hidden_states

    def __reorganize_states(self, hidden_states):
        """
        Reorganizes our hidden states such that state 0 = Not ovulating and State 1 = Ovulating
        :param hidden_states: The hidden state output from model prediction.
        :return: All relevant information for the model's prediction
        """
        assert self.model
        mus = np.array(self.model.means_)
        sigmas = np.array(np.sqrt(np.array([np.diag(self.model.covars_[0]), np.diag(self.model.covars_[1])])))
        P = np.array(self.model.transmat_)
        # Reorganize our resultant data so that the lower means lead to no ovulation and higher means lead to ovulation
        # The reason why it is like this is because the basis for this project is that higher basal body temps => ovulation
        # Therefore higher means would indicate higher temps thus based on our project this should indicate ovulation
        if mus[0] > mus[1]:
            mus = np.flipud(mus)
            sigmas = np.flipud(sigmas)
            P = np.fliplr(np.flipud(P))
            hidden_states = 1 - hidden_states

        return mus, sigmas, P, hidden_states

    def plot_results(self, hidden_states):
        """
        Plots the prediction results
        :param hidden_states: Predicted Hidden States from model
        :return: N/A
        """

        # This will be our y axis
        means = self.workData.flatten()

        # Use Seaborn for clean visualization
        sns.set()

        # Initialize our figure
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Create our x axis
        x_labels = [item[5:] for subList in self.dates for item in subList] # Use our dates as labels
        x_ticks = np.arange(len(means)) # The total number of means we have are the total number of predictions made

        masks0 = hidden_states == 0 # Seperate out state 0 (Not Ovulating) and plot it with red dots
        ax.scatter(x_ticks[masks0], means[masks0], c='r', label="Not Ovulating")

        # Separate out state 1 (Ovulating) and plot it with blue dots
        masks1 = hidden_states == 1
        ax.scatter(x_ticks[masks1], means[masks1], c='b', label="Ovulating")

        # Chart formatting
        plt.xticks(x_ticks, x_labels)
        plt.plot(x_ticks, means, c='k')
        plt.title("HMM Predictions using mostly good data") # Should change this to be robust
        ax.set_xlabel("Date")
        ax.set_ylabel("Daily Means")
        handles, labels = plt.gca().get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', ncol=2, frameon=True)

        # Finally show our results
        plt.show()

    def saveModel(self, outputFile="Ovu_Model.pkl"):
        """
        Saves our trained model in a pickle file
        :param outputFile: The filename of the model file
        :return: N/A
        """
        assert self.model
        if not self.loadedModel:
            with open(outputFile, 'wb') as file:
                pickle.dump(self.model, file)

    def loadModel(self, file_path):
        """
        Loads in a previously trained model from a pickle file
        :return: the loaded model
        """
        if hasattr(self, "model"):
            assert self.model is None

        with open(file_path, 'rb') as file:
            self.model = pickle.load(file)

def main():
    hasTime = False
    loadModel = None
    dir = askDir()

    # Input breaks file dialog, so askstring is just a replacement for that
    timeCheck = simpledialog.askstring(title="Ask Time", prompt="Does the file name have the time in it (hours, minutes, seconds)? [y/n] Default is n: ")
    if timeCheck == "y":
        hasTime = True

    askModel = simpledialog.askstring(title="Ask Model", prompt="Do you want to load in a model? [y/n] Default is n: ")
    if askModel == "y":
        print("Poop")
        loadModel = filedialog.askopenfilename()
        assert loadModel

    predictor = PredictorModel(dir, hasTime, loadModel)

    if not loadModel:
        predictor.train()

    mus, sigmas, P, logprob, samples, hidden_states = predictor.predict(1)

    predictor.saveModel()

    predictor.plot_results(hidden_states)
    print(predictor.model.transmat_)
    # predictor.saveModel()



if __name__ == "__main__":
    main()