from utils import *

Emotions = {1: "Anger",
            2: "Contempt",
            3: "Disgust",
            4: "Fear",
            5: "Happy",
            6: "Sadness",
            7: "Surprise"
            }
# Ottenimento delle cartelle che contengono le label delle emozioni di ogni soggetto
PATH_EMOTION = "Dataset/Emotion"
DatasetEmotion = getDirectories(PATH_EMOTION)
DISTANCE_NAME = "_GD_euclidean"
DISTANCE_TYPEDIR = "Global_Distances/"
DISTANCES_FLAG = 1
LANDMARKS_FLAG = 0
EMOTIONS_NUMBER = 7
# dizionario che mantiene le emozioni con i diversi soggetti,
# quindi le chiavi sono le emozioni ed i valori tutti i soggetti di quella emozione
emotion_dictionary = subjects_per_emotion(DatasetEmotion, DISTANCE_NAME)

def significative_values(flag_sign, distance_dir, emotion, emotion_subject):
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
        distances, signLandmarks = process_threshold_landmarks(s, emotion, frameSequence)
        if flag_sign == DISTANCES_FLAG:  # distances
            emotion_dict[s[:8]] = distances
        elif flag_sign == LANDMARKS_FLAG:  # landmarks
            directions = landmarks_XYdirections(s[:8], len(frameSequence.axes[0]) - 1)
            for i in signLandmarks:
                data = [i, directions[i][0], directions[i][1]]
                if s[:8] in emotion_dict:
                    emotion_dict[s[:8]].append(data)
                else:
                    emotion_dict[s[:8]] = [data]

    return emotion_dict


def get_emotion_similarities(flag_sign, emotion1, emotion2, distance_dir):
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

    emotion1_sign = significative_values(flag_sign, distance_dir, Emotions[emotion1], em1_subjects)

    if emotion1 == emotion2:
        emotion2_sign = emotion1_sign
    else:
        emotion2_sign = significative_values(flag_sign, distance_dir, Emotions[emotion2], em2_subjects)

    all_similarities = []
    if flag_sign == DISTANCES_FLAG: # distances
        for key1 in emotion1_sign:
            for key2 in emotion2_sign:
                if key1 == key2: continue
                sim = vectorSimilarity(emotion1_sign[key1], emotion2_sign[key2])
                all_similarities.append(sim)
    elif flag_sign == LANDMARKS_FLAG: # landmarks
        for key1 in emotion1_sign:
            for key2 in emotion2_sign:
                if key1 == key2: continue
                flat_em1 = [item for sublist in emotion1_sign[key1] for item in sublist]
                flat_em2 = [item for sublist in emotion2_sign[key2] for item in sublist]
                sim = vectorSimilarity(flat_em1, flat_em2)
                all_similarities.append(sim)

    return statistics.mean(all_similarities)


# print(emotion_dictionary)

print("CONFRONTO TRA EMOZIONI CONSIDERANDO LE DISTANZE O I LANDMARK SIGNIFICATIVE NELLE DISTANZE GLOBALI")
# confrontare le diverse emozioni di tutti i soggetti e visualizzare la similarità tra i landmark significativi estratti
for i in range(EMOTIONS_NUMBER):
    print("\n")
    for j in range(EMOTIONS_NUMBER):
        print("\nDISTANZE -> {} / {}: {}".format(Emotions[i + 1].upper(), Emotions[j + 1].upper(),
                                                             get_emotion_similarities(DISTANCES_FLAG, i + 1, j + 1, DISTANCE_TYPEDIR)))
        print("LANDMARK -> {} / {}: {}".format(Emotions[i + 1].upper(), Emotions[j + 1].upper(),
                                                                       get_emotion_similarities(LANDMARKS_FLAG, i + 1,
                                                                                                j + 1,
                                                                                                DISTANCE_TYPEDIR)))
