import os
import statistics
import random

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
def calculate_threshold(frame1, frame2):
    # CALCOLO threshold su landmark significativi per un solo soggetto e sola emozione
    # abbiamo preso la distanza (tra il secondo frame ed il primo) e la distanza (tra il frame individuato ed il primo), vedendo che dai landmark 200 ci sono delle distanze significative, quindi abbiamo calcolato
    # il delta (la differenza tra le distanze) andando a calcolare la media e stabilira una soglia.
    # # successivamente abbiamo visto quali landmark (prendendo la distanza dei frame considerati) superano la soglia e li abbiamo mostrati sul grafico
    # il concetto si basa sul considerare le distanze, tra:
    # - secondo frame e il primo (da posizione neutrale ad inizio micro-espressione)
    # - frame individuato (visivamente o applicando qualche concetto statistico, da valutare), in cui si ha un cambiamento di espressione significativo, e il primo
    # visualizziamo sul grafico quali landmark sono significativi, quindi quelli che hanno subito una maggiore variazione
    # andiamo a considerare l'intervallo di questi landmark e calcoliamo il delta, ovvero la differenza tra distanze
    # calcoliamo la media di questi valori (delta) e la consideriamo come soglia che i landmark devono superare per essere considerati significativi
    delta_distances = []
    for i in range(0, 468):
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

def get_distances_overT(frame, threshold):
    distances_overT = []
    landmarks = []
    for i in range(0,468):
        if frame[i] > threshold:
            distances_overT.append(frame[i])
            landmarks.append(i)
    return distances_overT, landmarks

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
    distances_FirstFrame = videoSequence_global.iloc[1:2, :468].values.tolist()
    flat_distances_first = [item for sublist in distances_FirstFrame for item in sublist]

    # numero di righe che indica il numero di frame
    number_rows = len(videoSequence_global.axes[0])

    distances_LastFrame = videoSequence_global.iloc[number_rows-1:number_rows, :468].values.tolist()
    flat_distances_last = [item for sublist in distances_LastFrame for item in sublist]
    # maxDistance =  max(flat_distances)
    # threshold = maxDistance - ((maxDistance * 5) /100) # prendiamo il 20% dei landmark più alti

    threshold = calculate_threshold(flat_distances_first, flat_distances_last)

    # plot_landmark(subject, videoSequence_global, flat_list_frame1, frame2, threshold)
    distances_overT, significative_Landmarks = get_distances_overT(flat_distances_last,threshold)
    return significative_Landmarks

Dataset_Emotion = getDirectories("Dataset/Emotion")
emotion_dictionary = {}
for dir in Dataset_Emotion:
    for file in os.listdir(dir):
        if os.path.basename(file).find('emotion') != -1:
            subject = file[:8]+"_GD_euclidean.csv"
            filename = os.path.join(dir,file)
            f = open(filename, "r")
            string_formatted = float(f.read().strip())
            f.close()
            if string_formatted in emotion_dictionary:
                emotion_dictionary[string_formatted].append(subject)
            else:
                emotion_dictionary[string_formatted] = [subject]

# print(emotion_dictionary)

def get_similarities(emotion1, emotion2):
    emotion1_subjects = emotion_dictionary[emotion1]
    emotion1_significant_landmarks = {}
    emotion2_subjects = emotion_dictionary[emotion2]
    emotion2_significant_landmarks = {}

    for s in emotion1_subjects:
        videoSequence_global = pd.read_csv("Global_Distances/" + s, header=None)
        significativeLandmarks = process_threshold_landmarks(videoSequence_global)
        emotion1_significant_landmarks[s[:8]] = significativeLandmarks
    if emotion1 == emotion2:
        emotion2_significant_landmarks = emotion1_significant_landmarks
    else:
        for s in emotion2_subjects:
            videoSequence_global = pd.read_csv("Global_Distances/" + s, header=None)
            significativeLandmarks = process_threshold_landmarks(videoSequence_global)
            emotion2_significant_landmarks[s[:8]] = significativeLandmarks

    all_similarities = []
    for key1 in emotion1_significant_landmarks:
        for key2 in emotion2_significant_landmarks:
            if key1 == key2: continue
            sim = vectorSimilarity(emotion1_significant_landmarks[key1], emotion2_significant_landmarks[key2])
            all_similarities.append(sim)

    return statistics.mean(all_similarities)

print("Emozione: Felicità")
print("Media di similarità nell'emozione Felicità: {}".format(get_similarities(5.0, 5.0)))

print("Emozione: rapporto Felicità / Paura")
print("Media di similarità nell'emozione Felicità: {}".format(get_similarities(5.0, 4.0)))

print("Emozione: rapporto Felicità / Tristezza")
print("Media di similarità nell'emozione Felicità: {}".format(get_similarities(5.0, 6.0)))

print("Emozione: rapporto Felicità / Disgusto")
print("Media di similarità nell'emozione Felicità: {}".format(get_similarities(5.0, 3.0)))

print("Emozione: rapporto Felicità / Rabbia")
print("Media di similarità nell'emozione Felicità: {}".format(get_similarities(5.0, 1.0)))

print("Emozione: rapporto Felicità / Disprezzo")
print("Media di similarità nell'emozione Felicità: {}".format(get_similarities(5.0, 2.0)))

print("Emozione: rapporto Felicità / Sorpresa")
print("Media di similarità nell'emozione Felicità: {}".format(get_similarities(5.0, 7.0)))