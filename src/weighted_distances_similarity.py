import random

from utils import *
import pandas as pd

Emotions = {1: "Anger",
            2: "Contempt",
            3: "Disgust",
            4: "Fear",
            5: "Happy",
            6: "Sadness",
            7: "Surprise"
            }

path_emotion = "Dataset/Emotion"
Dataset_Emotion = get_directories(path_dataset=path_emotion)
distance_name = "_GD_euclidean"
distance_typedir = "Global_Distances/"

emotion_dictionary = subjects_per_emotion(Dataset_Emotion=Dataset_Emotion, distance_name=distance_name)
del emotion_dictionary[0]

SPLIT_PERCENT = 0.8
NUMBER_EMOTION = 7
NUMBER_IT = 10
columns = {1: [0, 0, 0, 0, 0, 0, 0],
           2: [0, 0, 0, 0, 0, 0, 0],
           3: [0, 0, 0, 0, 0, 0, 0],
           4: [0, 0, 0, 0, 0, 0, 0],
           5: [0, 0, 0, 0, 0, 0, 0],
           6: [0, 0, 0, 0, 0, 0, 0],
           7: [0, 0, 0, 0, 0, 0, 0],
           }
df_weight = pd.DataFrame(columns, index=[1,2,3,4,5,6,7])
df_weight = df_weight.astype(float)

def get_distances(distance_dir, emotion_subject):
    """
                funzione che estrae per ogni soggetto di ogni emozione, le distanze dell'ultimo frame

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
    em1_subjects = emotion_training_dictionary[emotion1]

    # ottengo tutti i soggetti dell'emozione 2
    em2_subjects = emotion_training_dictionary[emotion2]

    # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 1
    em1_sign_land = get_distances(distance_dir=distance_dir, emotion_subject=em1_subjects)
    # print(em1_sign_land)
    if emotion1 == emotion2:
        # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 2
        em2_sign_land = em1_sign_land
    else:
        # dizionario che contiene i landmark (con le direzioni) per ogni soggetti della emozione 2
        em2_sign_land = get_distances(distance_dir=distance_dir, emotion_subject=em2_subjects)

    all_similarities = []
    for key1 in em1_sign_land:
        for key2 in em2_sign_land:
            if key1 == key2: continue
            flat_em1 = em1_sign_land[key1]
            flat_em2 = em2_sign_land[key2]
            sim = vector_similarity(v1=flat_em1, v2=flat_em2)
            all_similarities.append(sim)

    return statistics.mean(all_similarities)




def mean_emotion_vector(emotion, distance_dir):
    """
            funzione che estrae per ogni emozione il vettore media di tutte le distanze globali tra i soggetti di quella emozione
           - **Returns**:
           - **Value return** has type
           - Parameter **values**:
           - **Precondition**:
           """
    emotion_subjects = emotion_training_dictionary[emotion]
    emotion_distances = get_distances(distance_dir=distance_dir, emotion_subject=emotion_subjects)

    df_emotion_distances = pd.DataFrame(emotion_distances).transpose()

    meanVector = []
    for i in range(0, 468):
        meanVector.append(df_emotion_distances[int(i)].mean())

    return meanVector


def max_occurence(em_df, idxmax_value):
    if idxmax_value[0] == idxmax_value[1] == idxmax_value[2]:
        return idxmax_value[0]
    elif idxmax_value[0] == idxmax_value[1] or idxmax_value[0] == idxmax_value[2]:
        return idxmax_value[0]
    elif idxmax_value[1] == idxmax_value[2]:
        return idxmax_value[1]
    else:
        diff = 0
        vector0 = em_df.iloc[idxmax_value[0] - 1]
        vector1 = em_df.iloc[idxmax_value[1] - 1]
        vector2 = em_df.iloc[idxmax_value[2] - 1]

        for j in range(3):
            diff += vector0[j+1] - vector1[j+1]
        if diff > 0:
            diff = 0
            for j in range(3):
                diff += vector1[j+1] - vector2[j+1]
            if diff > 0:
                return idxmax_value[1]
            else:
                return idxmax_value[2]
        else:
            diff = 0
            for j in range(3):
                diff += vector0[j+1] - vector2[j+1]
            if diff > 0:
                return idxmax_value[0]
            else:
                return idxmax_value[2]

        return max(count_max_index, key=count_max_index.get)


def emotion_prediction(emotions_meanVector, test_sub, distance_dir):
    """
            funzione che effettua una predizione dell'emozione su un soggetto preso a caso dal test set
           - **Returns**:
           - **Value return** has type
           - Parameter **values**:
           - **Precondition**:
           """

    em_predict = {}
    meanVectorSim = {}

    subject_distances = get_distances(distance_dir=distance_dir, emotion_subject=[test_sub])

    for i in sorted(emotions_meanVector):
        meanVectorSim['S' + str(i)] = vector_similarity(v1=subject_distances[test_sub[:8]], v2=emotions_meanVector[i])

    value_c = min(meanVectorSim.values()) / 50
    for i in meanVectorSim:
        if i == max(meanVectorSim, key=meanVectorSim.get):
            meanVectorSim[max(meanVectorSim, key=meanVectorSim.get)] += value_c
        else:
            meanVectorSim[i] -= value_c

    for i in range(len(meanVectorSim)):
        multi_diagonal = meanVectorSim['S' + str(i + 1)] * 100 * df_weight[i + 1][i + 1]
        multi_weight = multi_diagonal

        sim_mean_column = []
        for j in range(len(df_weight.axes[0])):
            sim_mean_column.append(meanVectorSim['S' + str(i + 1)] * 100 * df_weight[j + 1][i + 1])
            if j == i: continue
            multi_weight -= df_weight[j + 1][i + 1]

        em_predict[i + 1] = [multi_diagonal, statistics.mean(sim_mean_column), multi_weight]

    em_df = pd.DataFrame(em_predict, index=[1, 2, 3]).transpose()

    highest_fc = em_df[1].nlargest(2).index.tolist();
    highest_sc = em_df[2].nlargest(2).index.tolist();
    highest_tc = em_df[3].nlargest(2).index.tolist()

    emotion_predicted = []
    for i in range(2):
        idxmax_value = [highest_fc[i], highest_sc[i], highest_tc[i]]
        emotion_predicted.append(max_occurence(em_df, idxmax_value))

    emotion_subject_label = [key for key, val in emotion_dictionary.items() if any(test_sub[:8] in s for s in val)]
    label = emotion_subject_label[0]

    if label not in accuracy_per_emotion:
        accuracy_per_emotion[label] = [0, 0]
    if label in emotion_predicted:
        accuracy_per_emotion[label][0] += 1
        accuracy_per_emotion[label][1] += 1
        return 1
    else:
        accuracy_per_emotion[label][1] += 1
        return 0

mean_accuracy = []
for number_split in range(NUMBER_IT):
    emotion_training_dictionary = {}
    test_subjects = []
    for key in emotion_dictionary:
        random.shuffle(emotion_dictionary[key])
        subjects = emotion_dictionary[key]
        emotion_training_dictionary[key] = subjects[:int(len(subjects) * SPLIT_PERCENT)]
        test_subjects.append(subjects[int(len(subjects) * SPLIT_PERCENT):])

    test_subjects = [item for sublist in test_subjects for item in sublist]
    for i in range(NUMBER_EMOTION):
        for j in range(NUMBER_EMOTION):
            df_weight[i + 1][j + 1] = get_emotion_similarities(i + 1, j + 1, distance_typedir)
    # estrazione vettori media distanze di ogni emozione
    emotions_meanVector = {}
    for i in range(NUMBER_EMOTION):
        emotions_meanVector[i + 1] = mean_emotion_vector(emotion=i + 1, distance_dir=distance_typedir)

    accuracy_per_emotion = {}
    emotion_prediction_results = []
    for s in test_subjects:
        emotion_prediction_results.append(emotion_prediction(emotions_meanVector=emotions_meanVector,
                                                             test_sub=s, distance_dir=distance_typedir))

    success = emotion_prediction_results.count(1)
    accuracy = (success / len(emotion_prediction_results)) * 100
    print(
        "N_SPLIT: {}, ACCURACY: {} - {}/{}".format(number_split, accuracy, success, len(emotion_prediction_results)))
    print("EMOTIONS_SUCCESS: ", accuracy_per_emotion)
    mean_accuracy.append(accuracy)

print("\nESEGUITE {} ITERAZIONI, L'ACCURATEZZA RISULTANTE È: {}".format(NUMBER_IT, statistics.mean(mean_accuracy)))


