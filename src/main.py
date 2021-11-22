import cluster
import model
from tkinter import Tk, filedialog

def time_constrain_files(timeStart, timeEnd, dir):
    return

def main():
    root = Tk()
    root.withdraw()

    root.attributes("-topmost", True)

    print("Please select the directory with the thermal images.")

    directory = filedialog.askdirectory()

    assert directory

    timeStart = 0 #TODO: Choose the starting time to filter out our image files
    timeEnd = 0 #TODO: Choose the ending time for filtering out our image files

    clusterer = cluster.clusterMaker(time_constrain_files(timeStart, timeEnd, directory))

    clusteredDir = clusterer.save_images_to_directory(clusterer.cluster_directory_images())



if __name__ == "__main__":
    main()