from matplotlib import pyplot as plt
import os
import pandas as pd

def plot_frames_landmarks(distance_name, video_sequence, index_first_frame, index_second_frame):
    """
                    This function create plots all the distances of landmarks belonging to two different frames.
                    Distances belonging to first frame are shown in blue while distnces belonging to frame two are
                    shown in red.

                   - Parameter **distanceName**: String. name of the metric used as a distance
                   - Parameter **videoSequence**: csv containing all the distances of a video sequence
                   - Parameter **indexFirstFrame**: index of the first frame to be considered
                   - Parameter **indexSecondFrame**: index of the second frame to be considered

    """

    for i in range(len(video_sequence.columns) - 2):
        plt.plot(i, video_sequence.iloc[index_first_frame, i], color='blue', marker='o')  # first frame
        plt.plot(i, video_sequence.iloc[index_second_frame, i], color='red', marker='^')  # frame of interest

    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel(distance_name, fontsize=14)
    plt.grid(True)
    plt.show()

def plot_significative_landmarks(distance_name, subject, video_sequence, distances, x_axis):
    """
                    This function creates a plot depicting all the landmarks belonging to the first frame and all the significant landmarks
                    belonging to the frame of interest.
                   - Parameter **distanceName**: String. name of the metric used as a distance
                   - Parameter **subject**: String. name of the subject
                   - Parameter **videoSequence**: Dataframe. Videosequence containg all the distances.
                   - Parameter **distances**: list of distances
                   - Parameter **xAxis**: axis to be considered, X in this case
    """
    for i in range(len(video_sequence.columns) - 2):
        plt.plot(i, video_sequence.iloc[1, i], color='blue', marker='o') # first frame
        if i in x_axis:
            plt.plot(i, distances[x_axis.index(i)], color='red', marker='^') # landmarks that have crossed the threshold

    plt.title(subject)
    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel(distance_name, fontsize=14)
    plt.grid(True)
    plt.show()

def plot_scatter3D(subject, emotion, landmarks_involved, index_frame):
    """
                    This function creates a plots where all the landmarks belonging to the first frame and all the landmarks belonging
                    to the significant frame are shown. We use blue to depict first landmarks and red the significant landmarks. This plot is in 3D.
                   - Parameter **subject**:
                   - Parameter **emotion**:
                   - Parameter **landmarksInvolved**:
                    - Parameter **indexFrame**:
        """
    sub_csv = []
    path_frames = "frames_csv/"
    for file in os.listdir(path_frames):
        if file.startswith(subject):
            sub_csv.append(os.path.join(path_frames, file))
    sub_csv = sorted(sub_csv)

    ff = pd.read_csv(sub_csv[0])
    lf = pd.read_csv(sub_csv[index_frame])

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')

    coordx_lf = []
    coordy_lf = []
    coordz_lf = []

    for val in landmarks_involved:
        coordx_lf.append(lf.iloc[val:val + 1, :1])
        coordy_lf.append(lf.iloc[val:val + 1, 1:2])
        coordz_lf.append(lf.iloc[val:val + 1, 2:3])


    ax.scatter3D(coordx_lf, coordy_lf, coordz_lf, color='red')
    ax.scatter3D(ff['x'], ff['y'], ff['z'], color='blue', alpha=0.2)
    plt.title("Person: " + subject + " Emotion: " + str(emotion))
    ax.set_axis_off()
    plt.show()

def plot_subjects_results(data):
    """
                    This function shows the number of occurencies of each video sequence, for all the subjects in the dataset
                   - Parameter **data**:

    """
    list_axisX = []
    for key in data:
        list_axisX.append(str(data[key][0]))
    axisX = set(list_axisX)
    plt.hist(sorted(list_axisX), bins=len(axisX))
    plt.ylabel('Soggetti')
    plt.xlabel('Sequenze frame')
    plt.title('Micro-espressione rilevata')
    plt.show()