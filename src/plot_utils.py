from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
# creazione grafico in cui mostriamo i landmark tra due frame di interesse
def plot_frames_landmarks(distanceName, videoSequence, indexFirstFrame, indexSecondFrame):
    for i in range(len(videoSequence.columns) - 2):
        plt.plot(i, videoSequence.iloc[indexFirstFrame, i], color='blue', marker='o')  # primo frame
        plt.plot(i, videoSequence.iloc[indexSecondFrame, i], color='red', marker='^')  # frame di interesse

    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel(distanceName, fontsize=14)
    plt.grid(True)
    plt.show()

# creazione grafico in cui mostriamo i landmark del primo frame e quelli significativi del frame di interesse
def plot_significative_landmarks(distanceName, subject, videoSequence, distances, xAxis):

    for i in range(len(videoSequence.columns)-2):
        plt.plot(i, videoSequence.iloc[1, i], color='blue', marker='o') # primo frame
        if i in xAxis:
            plt.plot(i, distances[xAxis.index(i)], color='red', marker='^') # landmark che hanno superato la soglia

    plt.title(subject)
    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel(distanceName, fontsize=14)
    plt.grid(True)
    plt.show()


def pvaluePlotter(Pvalue_history, splits):
    """
    This Function takes a list of pvalues and a list of splits where these pvalues where calculated and
    creates a plot showing how pvalue changed according to the several splits.
        - **Returns**: nothing

        - Parameter **Pvalue_history**: a list of pvalues

        - Parameter **splits**: a list of the split points where the pvalues where valuated

        - **Precondition**: Pvalue_history and splits are lists of numbers
    """
    x = np.array(splits)
    y = np.array(Pvalue_history)
    plt.ylabel("pvalue")
    plt.plot(x, y, color="red", marker="o", label="pvalue")
    plt.legend()
    plt.show()


def histogramPlotter(data):
    """
     This Function takes a list of values and uses plt.hist() to plot them
         - **Returns**: nothing

         - Parameter **data**: a list of pvalues


         - **Precondition**: list of values
     """
    plt.hist(data)
    plt.show()


def plot_scatter3D(subject, emotion, landmarksInvolved):
    sub_csv = []
    path_frames = "frames_csv/"
    for file in os.listdir(path_frames):
        if file.startswith(subject):
            sub_csv.append(os.path.join(path_frames, file))
    sub_csv = sorted(sub_csv)

    ff = pd.read_csv(sub_csv[0])
    lf = pd.read_csv(sub_csv[len(sub_csv)-1])

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')

    coordx_lf = []
    coordy_lf = []
    coordz_lf = []

    for val in landmarksInvolved:
        coordx_lf.append(lf.iloc[val:val + 1, :1])
        coordy_lf.append(lf.iloc[val:val + 1, 1:2])
        coordz_lf.append(lf.iloc[val:val + 1, 2:3])

    ax.scatter3D(ff['x'], ff['y'], ff['z'], color='blue')
    ax.scatter3D(coordx_lf, coordy_lf, coordz_lf, color='red')
    plt.title("Person: " + subject + " Emotion: " + str(emotion))
    plt.show()