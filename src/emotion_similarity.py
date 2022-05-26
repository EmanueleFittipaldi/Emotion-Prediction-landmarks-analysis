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
DatasetEmotion = get_directories(PATH_EMOTION)
DISTANCE_NAME = "_GD_euclidean"
DISTANCE_TYPEDIR = "Global_Distances/"
DISTANCES_FLAG = 1
LANDMARKS_FLAG = 0
EMOTIONS_NUMBER = 7
# dizionario che mantiene le emozioni con i diversi soggetti,
# quindi le chiavi sono le emozioni ed i valori tutti i soggetti di quella emozione
emotion_dictionary = subjects_per_emotion(Dataset_Emotion=DatasetEmotion, distance_name=DISTANCE_NAME)

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
        distances, signLandmarks = process_threshold_landmarks(subject=s, emotion=emotion, frameSeq=frameSequence)
        if flag_sign == DISTANCES_FLAG:  # distances
            emotion_dict[s[:8]] = distances
        elif flag_sign == LANDMARKS_FLAG:  # landmarks
            directions = landmarks_XYdirections(subject=s[:8], indexFrame=len(frameSequence.axes[0]) - 1)
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

    emotion1_sign = significative_values(flag_sign=flag_sign, distance_dir=distance_dir,
                                         emotion=Emotions[emotion1], emotion_subject=em1_subjects)

    if emotion1 == emotion2:
        emotion2_sign = emotion1_sign
    else:
        emotion2_sign = significative_values(flag_sign=flag_sign, distance_dir=distance_dir,
                                             emotion=Emotions[emotion2], emotion_subject=em2_subjects)

    all_similarities = []
    if flag_sign == DISTANCES_FLAG: # distances
        for key1 in emotion1_sign:
            for key2 in emotion2_sign:
                if key1 == key2: continue
                sim = vector_similarity(v1=emotion1_sign[key1], v2=emotion2_sign[key2])
                all_similarities.append(sim)
    elif flag_sign == LANDMARKS_FLAG: # landmarks
        for key1 in emotion1_sign:
            for key2 in emotion2_sign:
                if key1 == key2: continue
                flat_em1 = [item for sublist in emotion1_sign[key1] for item in sublist]
                flat_em2 = [item for sublist in emotion2_sign[key2] for item in sublist]
                sim = vector_similarity(v1=flat_em1, v2=flat_em2)
                all_similarities.append(sim)

    return statistics.mean(all_similarities)


# print(emotion_dictionary)
columns = { 1: [0, 0, 0, 0, 0, 0, 0],
            2: [0, 0, 0, 0, 0, 0, 0],
            3: [0, 0, 0, 0, 0, 0, 0],
            4: [0, 0, 0, 0, 0, 0, 0],
            5: [0, 0, 0, 0, 0, 0, 0],
            6: [0, 0, 0, 0, 0, 0, 0],
            7: [0, 0, 0, 0, 0, 0, 0],
            }
df_landmarks = pd.DataFrame(columns, index=[1, 2, 3, 4, 5, 6, 7])
df_landmarks = df_landmarks.astype(float)

df_distances = pd.DataFrame(columns, index=[1, 2, 3, 4, 5, 6, 7])
df_distances = df_distances.astype(float)

# confrontare le diverse emozioni di tutti i soggetti e visualizzare la similarità tra i landmark significativi estratti
for i in range(EMOTIONS_NUMBER):
    print("\n")
    for j in range(EMOTIONS_NUMBER):
        df_distances[i + 1][j + 1] = get_emotion_similarities(flag_sign=DISTANCES_FLAG, emotion1=i + 1,
                                                                                      emotion2=j + 1, distance_dir=DISTANCE_TYPEDIR)
        df_landmarks[i + 1][j + 1] = get_emotion_similarities(flag_sign=LANDMARKS_FLAG, emotion1=i + 1,
                                                              emotion2=j + 1, distance_dir=DISTANCE_TYPEDIR)

print("MATRICE SIM DISTANZE: \n", df_distances)
print("MATRICE SIM LANDMARK: \n", df_landmarks)

