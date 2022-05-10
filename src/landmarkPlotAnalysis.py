import statistics
import pandas as pd
from utils import *

# plotting 3D del primo frame (volto in posizione neutrale) e del frame che è stato individuato dal pvalue come significativo
# oppure dell'ultimo frame in cui si ha la massima macro-espressione
# first_frame = pd.read_csv('frames_csv/S999_003_00000001.csv')
# frame = pd.read_csv('frames_csv/S999_003_00000002.csv')
# # last_frame = pd.read_csv('frames_csv/S005_001_00000011.csv')
# print(first_frame)
# print(frame)
#
# fig = plt.figure(figsize=(12, 12))
# ax = fig.add_subplot(projection='3d')
#
# sequence_containing_x_vals = first_frame['x']
# sequence_containing_y_vals = first_frame['y']
# sequence_containing_z_vals = first_frame['z']
# sequence_frame_ind_x = []
# sequence_frame_ind_y = []
# sequence_frame_ind_z = []
#
# for val in landmarksInvolved:
#     sequence_frame_ind_x.append(frame.iloc[val:val+1, :1])
#     sequence_frame_ind_y.append(frame.iloc[val:val + 1, 1:2])
#     sequence_frame_ind_z.append(frame.iloc[val:val + 1, 2:3])
#
# ax.scatter3D(sequence_containing_x_vals, sequence_containing_y_vals, sequence_containing_z_vals, color='blue')
# ax.scatter3D(sequence_frame_ind_x, sequence_frame_ind_y, sequence_frame_ind_z, color='red')
#
# plt.show()

def plot_action_detected(videoSequence, indexFrame):
    # creazione grafico in cui mostriamo i landmark del primo frame (in blu e rappresentati da dei cerchi) e quelli del frame individuato
    # in cui si ha una variazione significativa da micro a macro espressione (in rosso e rappresentati dai triangoli)
    for i in range(len(videoSequence.columns) - 2):
        plt.plot(i, videoSequence.iloc[1, i], color='blue', marker='o')  # primo frame
        plt.plot(i, videoSequence.iloc[indexFrame, i], color='red', marker='^')  # frame di interesse

    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel('Global Distances', fontsize=14)
    plt.grid(True)
    plt.show()

def get_distances_overT(frame, threshold):
    distances_overT = []
    xAxis_distances = []
    for i in range(0,468):
        if frame[i] > threshold:
            distances_overT.append(frame[i])
            xAxis_distances.append(i)
    return distances_overT, xAxis_distances

def plot_landmark(subject, videoSequence, frame1, frame2, threshold):
    # creazione grafico in cui mostriamo i landmark del primo frame (in blu e rappresentati da dei cerchi) e solo i landmark significativi, del frame individuato
    # in cui si ha una variazione significativa da micro a macro espressione (in rosso e rappresentati dai triangoli)
    # struttura dati con le distanze che superano la soglia
    distances_overT, xAxis_distances = get_distances_overT(frame1, frame2, threshold)

    for i in range(len(videoSequence.columns)-2):
        plt.plot(i,videoSequence.iloc[1,i], color='blue', marker='o') # primo frame
        if i in xAxis_distances:
            plt.plot(i, distances_overT[xAxis_distances.index(i)], color='red', marker='^') # landmark che hanno superato la soglia
    plt.title(subject)
    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel('Global Distances', fontsize=14)
    plt.grid(True)
    plt.show()

def process_threshold_landmarks(videoSequence_global):

    # numero di righe che indica il numero di frame
    number_rows = len(videoSequence_global.axes[0])

    distances_LastFrame = videoSequence_global.iloc[number_rows-1:number_rows, :468].values.tolist()
    flat_distances = [item for sublist in distances_LastFrame for item in sublist]
    maxDistance =  max(flat_distances)
    threshold = maxDistance - ((maxDistance * 30) /100) # prendiamo il 20% dei landmark più alti
    print("treshod{}, maxdistance{}".format(threshold,maxDistance))

    # plot_landmark(subject, videoSequence_global, flat_list_frame1, frame2, threshold)
    distances_overT, significative_Landmarks = get_distances_overT(flat_distances,threshold)
    return significative_Landmarks



# Threshold_Fear = 0.0029133980764854835
# print("Soggetti: S999 - S504, Emozione: Paura")
# subject1 = "S504_004_GD_euclidean.csv"
# subject2 = "S999_003_GD_euclidean.csv"
# videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
# significativeLandmarks= process_threshold_landmarks(videoSequence_global)
# print(len(significativeLandmarks))
# videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
# significativeLandmarks= process_threshold_landmarks(videoSequence_global)
# print(len(significativeLandmarks))
# videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
# landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Fear)
# print("Landmark coinvolti nel soggetto 1: ", landmarks_involved1)
# print("Landmark coinvolti nel soggetto 2: ", landmarks_involved2)
# print("Percentuale di similarità tra due vettori: ", vectorSimilarity(landmarks_involved1, landmarks_involved2))

