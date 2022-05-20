import random
import statistics

from utils import *
import pandas as pd
Emotions = { 1 : "Anger",
             2 : "Contempt",
             3 : "Disgust",
             4 : "Fear",
             5 : "Happy",
             6 : "Sadness",
             7 : "Surprise"
             }

testSubjects = []
def get_distances(distance_dir, emotion_subject):
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
        dist_lf = frameSequence.iloc[-1, :468].values.tolist()
        emotion_dict[s[:8]] = dist_lf
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
    training_em1 = em1_subjects[:int(len(em1_subjects) * 0.8)]

    # ottengo tutti i soggetti dell'emozione 2
    em2_subjects = emotion_dictionary[emotion2]
    training_em2 = em2_subjects[:int(len(em2_subjects) * 0.8)]

    # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 1
    em1_sign_land = get_distances(distance_dir, training_em1)
    # print(em1_sign_land)
    if emotion1 == emotion2:
        # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 2
        em2_sign_land = em1_sign_land
    else:
        # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 2
        em2_sign_land = get_distances(distance_dir, training_em2)

    all_similarities = []
    for key1 in em1_sign_land:
        for key2 in em2_sign_land:
            if key1 == key2: continue
            flat_em1 = em1_sign_land[key1]
            flat_em2 = em2_sign_land[key2]
            sim = vectorSimilarity(flat_em1, flat_em2)
            all_similarities.append(sim)

    return statistics.mean(all_similarities)

def mean_emotion_vector(emotion, distance_dir):
    emotion_subects = emotion_dictionary[emotion]
    training_emotion = emotion_subects[:int(len(emotion_subects) * 0.8)]

    testing_emotion = emotion_subects[int(len(emotion_subects) * 0.8):]
    testSubjects.append(testing_emotion)

    emotion_distances = get_distances(distance_dir, training_emotion)

    df_emotion_distances = pd.DataFrame(emotion_distances).transpose()

    meanVector = []
    for i in range(0, 468):
        meanVector.append(df_emotion_distances[int(i)].mean())

    return meanVector


def emotion_prediction(emotions_meanVector, test_sub, distance_dir):
    print(test_sub)
    meanVectorSim = {}
    subject_distances = get_distances(distance_dir, [test_sub])
    for i in sorted(emotions_meanVector):
        meanVectorSim['S'+str(i)] = vectorSimilarity(subject_distances[test_sub[:8]], emotions_meanVector[i])
    print(meanVectorSim)
    mean_sim = []
    for i in range(len(meanVectorSim)):
        print("Moltiplicazione tra S{} e cella A({},{}): {}".format(i+1, i+1, i+1, meanVectorSim['S' + str(i + 1)] * df_weight[i+1][i+1]))
        sim = []
        for j in range(len(df_weight.axes[0])):
             sim.append(meanVectorSim['S' + str(i + 1)] * df_weight[j+1][i+1])
        mean_sim.append(statistics.mean(sim))
        print("Media rapporto similarità S{} e colonna {}: {}".format(i+1, i+1, statistics.mean(sim)))

# Ottenimento delle cartelle che contengono le label delle emozioni di ogni soggetto
path_emotion = "Dataset/Emotion"
Dataset_Emotion = getDirectories(path_emotion)
distance_name = "_GD_euclidean"
distance_typedir = "Global_Distances/"


# dizionario che mantiene le emozioni con i diversi soggetti,
# quindi le chiavi sono le emozioni ed i valori tutti i soggetti di quella emozione
emotion_dictionary = subjects_per_emotion(Dataset_Emotion, distance_name)

# estrazione vettori media distanze di ogni emozione
emotions_meanVector = {}
for i in range(7):
    emotions_meanVector[i+1] = mean_emotion_vector(i+1, distance_typedir)

print(emotions_meanVector)

# print(emotion_dictionary)

columns = { 1: [0.888355, 0.873252, 0.873308, 0.867073, 0.833290, 0.877848, 0.830290],
            2: [0.873252, 0.874211, 0.866920, 0.867197, 0.860873, 0.866558, 0.821439],
            3: [0.873308, 0.866920, 0.889282, 0.864420, 0.869549, 0.869607, 0.812009],
            4: [0.867073, 0.867197, 0.864420, 0.868243, 0.844843, 0.861261, 0.835643],
            5: [0.833290, 0.860873, 0.869549, 0.844843, 0.932606, 0.835797, 0.761870],
            6: [0.877848, 0.866558, 0.869607, 0.861261, 0.835797, 0.870114, 0.819227],
            7: [0.830290, 0.821439, 0.812009, 0.835643, 0.761870, 0.819227, 0.831948]
            }
df_weight = pd.DataFrame(columns, index=[1, 2, 3, 4, 5, 6, 7])
df_weight = df_weight.astype(float)
# confrontare le diverse emozioni di tutti i soggetti e visualizzare la similarità tra i landmark significativi estratti
# for i in range(7):
#     for j in range(7):
#         df_weight[i+1][j+1] = get_emotion_similarities(i+1, j+1, distance_typedir)

print(df_weight)

testSubjects = [item for sublist in testSubjects for item in sublist]
random.shuffle(testSubjects)
emotion_prediction(emotions_meanVector, random.choice(testSubjects), distance_typedir)