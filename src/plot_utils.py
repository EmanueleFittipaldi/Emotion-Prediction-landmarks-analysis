from matplotlib import pyplot as plt
import os
import pandas as pd

def plot_frames_landmarks(distanceName, videoSequence, indexFirstFrame, indexSecondFrame):
    """
                    funzione che permette di creare un grafico in cui mostriamo i landmark tra due frame di interesse
                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
        """

    for i in range(len(videoSequence.columns) - 2):
        plt.plot(i, videoSequence.iloc[indexFirstFrame, i], color='blue', marker='o')  # primo frame
        plt.plot(i, videoSequence.iloc[indexSecondFrame, i], color='red', marker='^')  # frame di interesse

    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel(distanceName, fontsize=14)
    plt.grid(True)
    plt.show()

def plot_significative_landmarks(distanceName, subject, videoSequence, distances, xAxis):
    """
                    funzione che permette di creare un grafico in cui mostriamo i landmark del primo frame e quelli significativi del frame di interesse
                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
        """
    for i in range(len(videoSequence.columns)-2):
        plt.plot(i, videoSequence.iloc[1, i], color='blue', marker='o') # primo frame
        if i in xAxis:
            plt.plot(i, distances[xAxis.index(i)], color='red', marker='^') # landmark che hanno superato la soglia

    plt.title(subject)
    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel(distanceName, fontsize=14)
    plt.grid(True)
    plt.show()

def plot_scatter3D(subject, emotion, landmarksInvolved, indexFrame):
    """
                    funzione che permette di creare un grafico in cui mostriamo i landmark del primo frame e quelli significativi
                    mostrando i punto su uno spazio tridimensionale
                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
        """
    sub_csv = []
    path_frames = "frames_csv/"
    for file in os.listdir(path_frames):
        if file.startswith(subject):
            sub_csv.append(os.path.join(path_frames, file))
    sub_csv = sorted(sub_csv)

    ff = pd.read_csv(sub_csv[0])
    lf = pd.read_csv(sub_csv[indexFrame])

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')

    coordx_lf = []
    coordy_lf = []
    coordz_lf = []

    for val in landmarksInvolved:
        coordx_lf.append(lf.iloc[val:val + 1, :1])
        coordy_lf.append(lf.iloc[val:val + 1, 1:2])
        coordz_lf.append(lf.iloc[val:val + 1, 2:3])


    ax.scatter3D(coordx_lf, coordy_lf, coordz_lf, color='red')
    ax.scatter3D(ff['x'], ff['y'], ff['z'], color='blue', alpha=0.2)
    plt.title("Person: " + subject + " Emotion: " + str(emotion))
    ax.set_axis_off()
    plt.show()