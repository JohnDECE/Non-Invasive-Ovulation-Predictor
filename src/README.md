### Non-Invasive Ovulation Predictor Software
NOTE: This software was built in python 3.9.2 using the hmmlearn library, scikit-learn and scikit-image libraries, as well as other helper libraries like os, matplotlib, and tkinter.
1. Obtain the dataset recorded using the recorder software and hardware
2. Run Cluster.py
   - It will ask for the dataset's directory, it will automatically generate an output directory in the dataset's directory after it is done with all the clustered and segmented images
3. Run model.py 
   
   - This will also ask for the dataset's directory, I recommend inputting the results from the clustering. If you already previously trained a model then you can also opt to load in that. The main function in this script should handle everything.
   
If you would like to just use the scripts as libraries, that will also work given that all of my code was put into classes. Just follow what was done in the main functions of each script to make them work.