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


def calculate_threshold(frame1, frame2, startLandmark, endLandmark):
    # CALCOLO threshold su landmark significativi per un solo soggetto e sola emozione
    # il concetto si basa sul considerare le distanze, tra:
    # - secondo frame e il primo (da posizione neutrale ad inizio micro-espressione)
    # - frame individuato (visivamente o applicando qualche concetto statistico, da valutare), in cui si ha un cambiamento di espressione significativo, e il primo
    # visualizziamo sul grafico quali landmark sono significativi, quindi quelli che hanno subito una maggiore variazione
    # andiamo a considerare l'intervallo di questi landmark e calcoliamo il delta, ovvero la differenza tra distanze
    # calcoliamo la media di questi valori (delta) e la consideriamo come soglia che i landmark devono superare per essere considerati significativi
    delta_distances = []
    for i in range(startLandmark, endLandmark):
        delta = frame2[i] - frame1[i]
        delta_distances.append(delta)

    return statistics.mean(delta_distances)

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

def get_distances_overT(frame1, frame2, threshold):
    distances_overT = []
    xAxis_distances = []
    for i in range(0,468):
        delta = frame2[i] - frame1[i]
        if delta > threshold:
            distances_overT.append(frame2[i])
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


def process_threshold_landmarks(subject, videoSequence_global, threshold):
    # Calcolo threshold per capire quanti landmark si sono aggiunti tra i diversi frame
    # per ogni frame (rispetto al primo) ottenere il numero di landmark che superano la soglia (sono quelli significativi)
    # successivamente calcolare le differenze tra questi numeri, per capire in quale frame si ha una maggiore aggiunta
    # di landmark significativi (probabilmente è in questo caso che si ha avuto una variazione da micro a macro espressione)
    # prima distanza (secondo frame ed il primo)
    list_values_frame1 = videoSequence_global.iloc[1:2,:468].values.tolist()
    flat_list_frame1 = [item for sublist in list_values_frame1 for item in sublist]
    # numero di righe che indica il numero di frame
    number_rows = len(videoSequence_global.axes[0])
    # valore in cui è contenuta la variazione più grande
    max_value = 0
    # numero del frame
    frame = 0
    # struttura dati che contiene numero di landmark significativi per ogni frame
    NSignificative_land = []
    for i in range(2, number_rows):
        # frame successivi
        list_frame2 = videoSequence_global.iloc[i:i+1, :468].values.tolist()
        frame2 = [item for sublist in list_frame2 for item in sublist]
        distances_overT, xAxis_distances = get_distances_overT(flat_list_frame1, frame2, threshold)
        NSignificative_land.append(len(distances_overT))

    print("\nSoggetto: ", subject)
    print("Numero di landmark significativi: {}, In ogni frame: {}".format(len(NSignificative_land),NSignificative_land))

    # calcolo delle differenze tra i numeri, per capire qual è il più grande
    for i in range(len(NSignificative_land)-1):
        delta = NSignificative_land[i+1] - NSignificative_land[i]
        if delta > max_value:
            max_value = delta
            frame = i+2

    print("Valore più grande di aggiunte: {}, nel frame: {}".format(max_value,frame))

    # frame in cui si è avuta la differenza maggiore
    list_frame2 = videoSequence_global.iloc[frame:frame+1, :468].values.tolist()
    frame2 = [item for sublist in list_frame2 for item in sublist]
    # plot dei landmark
    # plot_landmark(subject, videoSequence_global, flat_list_frame1, frame2, threshold)
    distances_overT, xAxis_distances = get_distances_overT(flat_list_frame1, frame2, threshold)
    return xAxis_distances


Threshold_Fear = 0.0029133980764854835
print("Soggetti: S999 - S504, Emozione: Paura")
subject1 = "S504_004_GD_euclidean.csv"
subject2 = "S999_003_GD_euclidean.csv"
videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
landmarks_involved1 = process_threshold_landmarks(subject1,videoSequence_global, Threshold_Fear)
videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Fear)
print("Landmark coinvolti nel soggetto 1: ", landmarks_involved1)
print("Landmark coinvolti nel soggetto 2: ", landmarks_involved2)
print("Percentuale di similarità tra due vettori: ", vectorSimilarity(landmarks_involved1, landmarks_involved2))

print("\nSoggetti: S014 - S022, Emozione: Felicità")
subject1 = "S014_001_GD_euclidean.csv"
subject2 = "S022_001_GD_euclidean.csv"
videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
landmarks_involved1 = process_threshold_landmarks(subject1,videoSequence_global, Threshold_Fear)
videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Fear)
print("Landmark coinvolti nel soggetto 1: ", landmarks_involved1)
print("Landmark coinvolti nel soggetto 2: ", landmarks_involved2)
print("Percentuale di similarità tra due vettori: ", vectorSimilarity(landmarks_involved1, landmarks_involved2))


print("\nSoggetti: S129 - S506, Emozione: S129 -> disgusto, S506 -> rabbia")
subject1 = "S129_001_GD_euclidean.csv"
subject2 = "S506_001_GD_euclidean.csv"
videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
landmarks_involved1 = process_threshold_landmarks(subject1,videoSequence_global, Threshold_Fear)
videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Fear)
print("Landmark coinvolti nel soggetto 1: ", landmarks_involved1)
print("Landmark coinvolti nel soggetto 2: ", landmarks_involved2)
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
# Threshold_Angry = calculate_threshold(flat_list_frame1, flat_list_frame2, 0, 468)
Threshold_Angry = 0.00510002471554812
print("Threshold Andry:", Threshold_Angry)
print("\nSoggetti: S129 - S506, Emozione: S129 -> disgusto, S506 -> rabbia")
subject1 = "S129_001_GD_euclidean.csv"
subject2 = "S506_001_GD_euclidean.csv"
videoSequence_global = pd.read_csv("Global_Distances/"+subject1, header=None)
landmarks_involved1 = process_threshold_landmarks(subject1,videoSequence_global, Threshold_Angry)
videoSequence_global = pd.read_csv("Global_Distances/"+subject2, header=None)
landmarks_involved2 = process_threshold_landmarks(subject2,videoSequence_global, Threshold_Angry)
print("Landmark coinvolti nel soggetto 1: ", landmarks_involved1)
print("Landmark coinvolti nel soggetto 2: ", landmarks_involved2)
print("Percentuale di similarità tra due vettori: ", vectorSimilarity(landmarks_involved1, landmarks_involved2))