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


def getThreshold(flat_list_frame1, flat_list_frame2, startLandmark, endLandmark):
    # CALCOLO threshold su landmark significativi per un solo soggetto e sola emozione
    # abbiamo preso la distanza (tra il secondo frame ed il primo) e la distanza (tra il frame individuato ed il primo), vedendo che dai landmark 200 ci sono delle distanze significative, quindi abbiamo calcolato
    # il delta (la differenza tra le distanze) andando a calcolare la media e stabilira una soglia.
    # # successivamente abbiamo visto quali landmark (prendendo la distanza dei frame considerati) superano la soglia e li abbiamo mostrati sul grafico
    delta_distances = []
    for i in range(startLandmark,endLandmark):
        delta = flat_list_frame2[i] - flat_list_frame1[i]
        delta_distances.append(delta)

    return statistics.mean(delta_distances)

def plot_actionDetected(videoSequence, indexFrame):

    for i in range(len(videoSequence.columns) - 2):
        plt.plot(i, videoSequence.iloc[1, i], color='blue', marker='o')  # primo frame
        plt.plot(i, videoSequence.iloc[indexFrame, i], color='red', marker='^')  # frame di interesse

    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel('Global Distances', fontsize=14)
    plt.grid(True)
    plt.show()

def plot_landmark(subject, videoSequence, flat_list_frame1, flat_list_frame2, threshold):
    distances_overT = []
    xAxis_distances = []
    for i in range(0,468):
        delta = flat_list_frame2[i] - flat_list_frame1[i]
        if delta > threshold:
            distances_overT.append(flat_list_frame2[i])
            xAxis_distances.append(i)

    for i in range(len(videoSequence.columns)-2):
        plt.plot(i,videoSequence.iloc[1,i], color='blue', marker='o') # primo frame
        if i in xAxis_distances:
            plt.plot(i, distances_overT[xAxis_distances.index(i)], color='red', marker='^')  # ultimo frame
    plt.title(subject)
    plt.xlabel('Landmarks', fontsize=14)
    plt.ylabel('Global Distances', fontsize=14)
    plt.grid(True)
    plt.show()


def process_threshold_landmarks(subject, videoSequence_global, threshold):
    # Calcolo threshold per capire quanti landmark si sono aggiunti tra i diversi frame
    list_values_frame1 = videoSequence_global.iloc[1:2,:468].values.tolist()
    flat_list_frame1 = [item for sublist in list_values_frame1 for item in sublist]

    number_rows = len(videoSequence_global.axes[0])
    max_value = 0
    frame = 0
    number_significative_landmarks = []
    for i in range(2, number_rows):
        list_values_frame2 = videoSequence_global.iloc[i:i+1, :468].values.tolist()
        flat_list_frame2 = [item for sublist in list_values_frame2 for item in sublist]

        # successivamente abbiamo visto quali landmark (prendendo la distanza dei frame considerati) superano la soglia e li abbiamo mostrati sul grafico
        distances_overT = []
        xAxis_distances = []
        for j in range(0,468):
            delta = flat_list_frame2[j] - flat_list_frame1[j]
            if delta > threshold:
                distances_overT.append(flat_list_frame2[j])
                xAxis_distances.append(j)
        number_significative_landmarks.append(len(distances_overT))
    print("Soggetto: ", subject)
    print("Numero di landmark significativi: {}, In ogni frame: {}".format(len(number_significative_landmarks),number_significative_landmarks))
    for i in range(len(number_significative_landmarks)-1):
        delta = number_significative_landmarks[i+1] - number_significative_landmarks[i]
        if delta > max_value:
            max_value = delta
            frame = i+2

    print("Valore max di aumento: {}, frame: {}".format(max_value,frame))

    list_values_frame2 = videoSequence_global.iloc[frame:frame+1, :468].values.tolist()
    flat_list_frame2 = [item for sublist in list_values_frame2 for item in sublist]

    # plot_landmark(subject, videoSequence_global, flat_list_frame1, flat_list_frame2, threshold)
    return xAxis_distances


Threshold_Fear = 0.0029133980764854835
print("Soggetti: S999 - S504, Emozione: Paura")
subject1 = "S504_004_GD_euclidean.csv"
subject2 = "S999_003_GD_euclidean.csv"
videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
landmarks_involved1 = process_threshold_landmarks(subject1,videoSequence_global, Threshold_Fear)
videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Fear)

print("Percentuale di similarità tra due vettori: ", vectorSimilarity(landmarks_involved1, landmarks_involved2))

print("\nSoggetti: S014 - S022, Emozione: Felicità")
subject1 = "S014_001_GD_euclidean.csv"
subject2 = "S022_001_GD_euclidean.csv"
videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
landmarks_involved1 = process_threshold_landmarks(subject1,videoSequence_global, Threshold_Fear)
videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Fear)

print("Percentuale di similarità tra due vettori: ", vectorSimilarity(landmarks_involved1, landmarks_involved2))


print("\nSoggetti: S129 - S506, Emozione: S129 -> disgusto, S506 -> rabbia")
subject1 = "S129_001_GD_euclidean.csv"
subject2 = "S506_001_GD_euclidean.csv"
videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
landmarks_involved1 = process_threshold_landmarks(subject1,videoSequence_global, Threshold_Fear)
videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Fear)

print("Percentuale di similarità tra due vettori: ", vectorSimilarity(landmarks_involved1, landmarks_involved2))

# Calcolo threshold per angry (incazzato)
subject = "S506_001_GD_euclidean.csv"
videoSequence = pd.read_csv("Global_Distances/"+subject, header=None)
indexFrame = 4

list_values_frame1 = videoSequence.iloc[1:2, :468].values.tolist()
flat_list_frame1 = [item for sublist in list_values_frame1 for item in sublist]

list_values_frame2 = videoSequence.iloc[indexFrame:indexFrame+1, :468].values.tolist()
flat_list_frame2 = [item for sublist in list_values_frame2 for item in sublist]

# plot_actionDetected(videoSequence, indexFrame)
Threshold_Angry = getThreshold(flat_list_frame1, flat_list_frame2, 0, 468)
# Threshold_Angry = 0.00510002471554812
print("Threshold Andry:", Threshold_Angry)
print("\nSoggetti: S129 - S506, Emozione: S129 -> disgusto, S506 -> rabbia")
subject1 = "S129_001_GD_euclidean.csv"
subject2 = "S506_001_GD_euclidean.csv"
videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
landmarks_involved1 = process_threshold_landmarks(subject1,videoSequence_global, Threshold_Angry)
videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Angry)

print("Percentuale di similarità tra due vettori: ", vectorSimilarity(landmarks_involved1, landmarks_involved2))