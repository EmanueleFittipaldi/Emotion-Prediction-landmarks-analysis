from utils import *
import plot_utils as plot

Emotions = { 1 : "Anger",
             2 : "Contempt",
             3 : "Disgust",
             4 : "Fear",
             5 : "Happy",
             6 : "Sadness",
             7 : "Surprise"
             }

def get_distances_overT(frame, threshold):
    """
        ****
       - **Returns**:
       - **Value return** has type
       - Parameter **values**:
       - **Precondition**:
       """
    distances_overT = []
    landmarks = []
    for i in range(0,468):
        if frame[i] > threshold:
            distances_overT.append(frame[i])
            landmarks.append(i)
    return distances_overT, landmarks

def process_threshold_landmarks(subject, emotion, frameSeq):
    """
                   funzione che calcola la threshold e ottiene i landmark che superano la threshold

                  - **Returns**:
                  - **Value return** has type
                  - Parameter **values**:
                  - **Precondition**:
       """
    number_rows = len(frameSeq.axes[0])

    dist_ff = frameSeq.iloc[1:2, :468].values.tolist()
    fldist_ff = [item for sublist in dist_ff for item in sublist]

    dist_lf = frameSeq.iloc[number_rows-1:number_rows, :468].values.tolist()
    fldist_lf = [item for sublist in dist_lf for item in sublist]

    delta_distances = []
    for i in range(0, 468):
        delta = fldist_lf[i] - fldist_ff[i]
        delta_distances.append(delta)

    threshold = statistics.mean(delta_distances)

    distancesOverT, significativeLandmarks = get_distances_overT(fldist_lf, threshold)
    # plot.plot_significative_landmarks('Global Distances', subject, frameSeq, distancesOverT, significativeLandmarks)
    plot.plot_scatter3D(subject[:8], emotion, significativeLandmarks)

    return significativeLandmarks

def get_landmarks(distance_dir, emotion, emotion_subject):
    """
                funzione che estrae per ogni soggetto di ogni emozione, i landmark e le direzioni dei landmark

               - **Returns**:
               - **Value return** has type
               - Parameter **values**:
               - **Precondition**:
    """

    emotion_dict = {}

    for s in emotion_subject:
        frameSequence = pd.read_csv(distance_dir + s, header=None)
        signLandmarks = process_threshold_landmarks(s, emotion, frameSequence)
        directions = landmarks_XYdirections(s[:8], len(frameSequence.axes[0]) - 1)

        for i in signLandmarks:
            data = [i, directions[i][0], directions[i][1]]
            if s[:8] in emotion_dict:
                emotion_dict[s[:8]].append(data)
            else:
                emotion_dict[s[:8]] = [data]

    return emotion_dict

def get_emotion_similarities(emotion1, emotion2, distance_dir):
    """
            funzione che estrae per ogni soggetto di ogni emozione, i landmark significativi
            confronta i vettori di landmark (in cui sono incluse anche le direzioni) dando in output una percentuale di similarità

           - **Returns**:
           - **Value return** has type
           - Parameter **values**:
           - **Precondition**:
           """
    # ottengo tutti i soggetti dell'emozione 1
    em1_subjects = emotion_dictionary[emotion1]

    # ottengo tutti i soggetti dell'emozione 2
    em2_subjects = emotion_dictionary[emotion2]

    # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 1
    em1_sign_land = get_landmarks(distance_dir, Emotions[emotion1], em1_subjects)

    if emotion1 == emotion2:
        # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 2
        em2_sign_land = em1_sign_land
    else:
        # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 2
        em2_sign_land = get_landmarks(distance_dir, Emotions[emotion2], em2_subjects)

    all_similarities = []
    for key1 in em1_sign_land:
        for key2 in em2_sign_land:
            if key1 == key2: continue
            flat_em1 = [item for sublist in em1_sign_land[key1] for item in sublist]
            flat_em2 = [item for sublist in em1_sign_land[key2] for item in sublist]
            sim = vectorSimilarity(flat_em1, flat_em2)
            all_similarities.append(sim)

    return statistics.mean(all_similarities)


# Ottenimento delle cartelle che contengono le label delle emozioni di ogni soggetto
path_emotion = "Dataset/Emotion"
Dataset_Emotion = getDirectories(path_emotion)
distance_name = "_GD_euclidean"
distance_typedir = "Global_Distances/"


# dizionario che mantiene le emozioni con i diversi soggetti,
# quindi le chiavi sono le emozioni ed i valori tutti i soggetti di quella emozione
emotion_dictionary = {}
for dir in Dataset_Emotion:
    for file in os.listdir(dir):
        if os.path.basename(file).find('emotion') != -1:
            subject = file[:8]+distance_name+".csv"
            filename = os.path.join(dir, file)
            f = open(filename, "r")
            string_formatted = float(f.read().strip())
            f.close()
            if string_formatted in emotion_dictionary:
                emotion_dictionary[string_formatted].append(subject)
            else:
                emotion_dictionary[string_formatted] = [subject]

# print(emotion_dictionary)

# confrontare le diverse emozioni di tutti i soggetti e visualizzare la similarità tra i landmark significativi estratti
for i in range(7):
    print("\n")
    for j in range(7):
        print("Emozione_1: {}, Emozione_2: {}".format(Emotions[i+1], Emotions[j+1]))
        print("Rapport di similarità tra {} e {}: {}".format(Emotions[i+1], Emotions[j+1], get_emotion_similarities(i+1, j+1, distance_typedir)))
