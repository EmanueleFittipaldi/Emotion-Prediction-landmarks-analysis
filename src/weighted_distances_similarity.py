import random
from utils import *
import pandas as pd

EMOTIONS = {1: "Anger",
            2: "Contempt",
            3: "Disgust",
            4: "Fear",
            5: "Happy",
            6: "Sadness",
            7: "Surprise"
            }

PATH_EMOTION = "Dataset/Emotion"
DATASET_EMOTION = get_directories(path_dataset=PATH_EMOTION)
DISTANCE_NAME = "_GD_euclidean"
DISTANCE_DIR = "Global_Distances/"

# dictionary that maintains the emotions with the different subjects,
# so the keys are the emotions and values all the subjects of that emotion
emotion_dictionary = subjects_per_emotion(dataset_emotion=DATASET_EMOTION, distance_name=DISTANCE_NAME)
del emotion_dictionary[0]  # neutral expression deleted

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
# matrix (7x7) that contains the percentage of similarities between all emotions
df_weight = pd.DataFrame(columns, index=[1, 2, 3, 4, 5, 6, 7])
df_weight = df_weight.astype(float)


def get_distances(distance_dir, emotion_subject):
    """
    This Function takes as input a directory that contains distances (euclidean or manhattan) and a list of subjects of an emotion.
    Opens the CSVs of the distances of all subjects and extracts the distances of the last frame.
           - **Returns**: a dictionary in which key is a subject and values are distances.
           - **Value return** has type dict.
           - Parameter **values**: directory of the distances and a list of subjects.
           - **Precondition**: distance_dir must be a path string and emotion_subject type list.
    """
    emotion_dict = {}

    for s in emotion_subject:
        frameSequence = pd.read_csv(distance_dir + s, header=None)
        dist_lf = frameSequence.iloc[-1, :468].values.tolist()
        # key subject 'SXXX_XXX'
        emotion_dict[s[:8]] = dist_lf
    return emotion_dict


def get_emotion_similarities(emotion1, emotion2, distance_dir):
    """
    This Function takes as input two emotion key and a directory that contains distances.
    For each incoming emotion and for each subjects of an emotion, it extracts a distances list and calculates an average of similarities
    between these lists. The result is a percentage of similarity between two emotions.
           - **Returns**: A value that indicates a percentage of similarity (the average between all similarities).
           - **Value return** has type float.
           - Parameter **values**: two strings indicating the two emotions and a path of the distances directory.
           - **Precondition**: emotion1 and emotion2 must be a strings and distance_dir must be a path string.
           """
    # take all the subjects of emotion1 and emotion2 from dictionary of all emotions
    em1_subjects = emotion_training_dictionary[emotion1]
    em2_subjects = emotion_training_dictionary[emotion2]

    # dictionary that contains the vector of the distances of each subjects of emotion1 (same for emotion2)
    em1_sign_dist = get_distances(distance_dir=distance_dir, emotion_subject=em1_subjects)
    if emotion1 == emotion2:
        em2_sign_dist = em1_sign_dist
    else:
        em2_sign_dist = get_distances(distance_dir=distance_dir, emotion_subject=em2_subjects)

    # for each subject of emotion1 it calculates similarity with all the subjects of emotion2,
    # places the result in a list (all_similarities) and returns an average of all these similarities.
    all_similarities = []
    for key1 in em1_sign_dist:
        for key2 in em2_sign_dist:
            if key1 == key2: continue  # jump same subject
            sim = vector_similarity(v1=em1_sign_dist[key1], v2=em2_sign_dist[key2])
            all_similarities.append(sim)

    return statistics.mean(all_similarities)


def mean_emotion_vector(emotion, distance_dir):
    """
    This Function takes as input an emotion and a directory that contains distances.
    For each subjects of emotion extracts the distances, then for each landmark calculates an average of all these distances
    and places it in a vector.
        - **Returns**: a vector that contains an average of distances for each landmark of each emotion.
        - **Value return** has type list.
        - Parameter **values**: emotion of interest and a path of the distance directory.
        - **Precondition**: emotion must be a string and distance_dir must be a path string.
           """
    emotion_subjects = emotion_training_dictionary[emotion]
    emotion_distances = get_distances(distance_dir=distance_dir, emotion_subject=emotion_subjects)
    # creates a pandas dataframe in which columns are landmarks and a rows are frames.
    df_emotion_distances = pd.DataFrame(emotion_distances).transpose()

    mean_vector = []
    for column in range(0, 468):
        mean_vector.append(df_emotion_distances[int(column)].mean())

    return mean_vector


def max_occurence(em_df, idxmax_value):
    """
        This Function takes as input a dataframe that contains the values calculated with the three methods (multiplications with the diagonal,
         average of the multiplications between similarities of emotions and columns and the last method is a subtraction from the diagonal
         the remaining values of the corresponding columns) and a list of emotions predicted by these methods.
         The purpose of this function is to make a decision about which emotion to assign to a subject.
         If there is no majority calculates the sums of the differences between the values of these three predicted emotions and
         assign the emotion that has the greatest difference to a subject.
            - **Returns**: a value that indicates the predicted emotion.
            - **Value return** has type integer.
            - Parameter **values**: dataframe and a list of emotions predicted.
            - **Precondition**: idxmax_value must be a list of int.
    """
    # the first value of idxmax_value is am emotion predicted in the first method,
    # the second value is an emotion obtained by the second method
    # and the third value predicted in the last method.

    # all three values are equal
    if idxmax_value[0] == idxmax_value[1] == idxmax_value[2]:
        return idxmax_value[0]
    # two values are equal (still majority)
    elif idxmax_value[0] == idxmax_value[1] or idxmax_value[0] == idxmax_value[2]:
        return idxmax_value[0]
    elif idxmax_value[1] == idxmax_value[2]:
        return idxmax_value[1]
    # all three values are different, no majority
    else:
        # for each predicted emotion take the values calculated with three methods
        diff = 0
        vector0 = em_df.iloc[idxmax_value[0] - 1]
        vector1 = em_df.iloc[idxmax_value[1] - 1]
        vector2 = em_df.iloc[idxmax_value[2] - 1]

        # calculates the sum of differences between the values of the first emotion and the values of the second emotion
        for j in range(3):
            diff += vector0[j + 1] - vector1[j + 1]
        # if the difference is positive then the values of the first emotion are greater than the values of the second emotion
        # otherwise the opposite
        if diff > 0:
            diff = 0
            # calculates the sum of differences between the values of the second emotion and the values of the third emotion
            for j in range(3):
                diff += vector1[j + 1] - vector2[j + 1]
            # if the difference is positive then the values of the second emotion are greater than the values of the third emotion,
            # therefore the second emotion has the greatest difference and assign this to the subject
            # otherwise the third emotion is assigned
            if diff > 0:
                return idxmax_value[1]
            else:
                return idxmax_value[2]
        else:
            diff = 0
            # calculates the sum of differences between the values of the first emotion and the values of the third emotion
            for j in range(3):
                diff += vector0[j + 1] - vector2[j + 1]
            # if the difference is positive then the values of the first emotion are greater than the values of the third emotion,
            # therefore the first emotion has the greatest difference and assign this to the subject
            # otherwise the third emotion is assigned
            if diff > 0:
                return idxmax_value[0]
            else:
                return idxmax_value[2]

        return 0


def emotion_prediction(emotions_mean_vector, test_sub, distance_dir):
    """
    This Function takes as input a vector that contains an average of distances for each emotion, a test subject
    and a directory that contains distances.
    The purpose is predict the emotion of the subject taken from the training set.
       - **Returns**: 1 if the emotion predicted is correct, 0 otherwise.
       - **Value return** has type integer.
       - Parameter **values**: emotion_mean_vector is a list, test_sub is a string, distance_dir is a path of the distance directory.
       - **Precondition**: only one test subject in input.
       """
    # dictionary that maintains the values calculated by the three approaches for each emotion with respect to the test subject
    em_predict = {}
    mean_vector_sim = {}

    subject_distances = get_distances(distance_dir=distance_dir, emotion_subject=[test_sub])

    # for each emotion calculates the similarities between the distances of the subject and the average distances of the emotion
    for i in sorted(emotions_mean_vector):
        mean_vector_sim['S' + str(i)] = vector_similarity(v1=subject_distances[test_sub[:8]],
                                                          v2=emotions_mean_vector[i])
    # get the min and max similarities
    value_c = min(mean_vector_sim.values()) / 50
    max_sim = max(mean_vector_sim, key=mean_vector_sim.get)
    for sim in mean_vector_sim:
        # if is the max similarity, awards a prize that corresponds the min similarity divided by 50
        if sim == max_sim:
            mean_vector_sim[max_sim] += value_c
        # otherwise assigns a penalty of equal value
        else:
            mean_vector_sim[sim] -= value_c

    # calculates the values of the three methods
    for i in range(len(mean_vector_sim)):
        # multiplication between similarities calculated earlier and the values on the diagonal (FIRST METHOD)
        multi_diagonal = mean_vector_sim['S' + str(i + 1)] * 100 * df_weight[i + 1][i + 1]
        multi_weight = multi_diagonal
        # average of the multiplications between similarities and the column to the emotion taken into consideration (SECOND METHOD)
        sim_mean_column = []
        for j in range(len(df_weight.axes[0])):
            sim_mean_column.append(mean_vector_sim['S' + str(i + 1)] * 100 * df_weight[j + 1][i + 1])
            if j == i: continue # jump same emotion
            # subtracting from the multiplication with the diagonal the remaining values on the column match (THIRD METHOD)
            multi_weight -= df_weight[j + 1][i + 1]
        # the key is an emotion and the value is a list containing the results of three methods
        em_predict[i + 1] = [multi_diagonal, statistics.mean(sim_mean_column), multi_weight]

    em_df = pd.DataFrame(em_predict, index=[1, 2, 3]).transpose()

    # for each column (three methods values) get the first and second largest values
    highest_fc = em_df[1].nlargest(2).index.tolist();
    highest_sc = em_df[2].nlargest(2).index.tolist();
    highest_tc = em_df[3].nlargest(2).index.tolist()

    emotion_predicted = []
    # the two most probable emotions are considered and inserted into an array
    for i in range(2):
        idxmax_value = [highest_fc[i], highest_sc[i], highest_tc[i]]
        emotion_predicted.append(max_occurence(em_df, idxmax_value))

    # get the emotion label of the test subject
    emotion_subject_label = [key for key, val in emotion_dictionary.items() if any(test_sub[:8] in s for s in val)]
    label = emotion_subject_label[0]

    if label not in accuracy_per_emotion:
        accuracy_per_emotion[label] = [0, 0]
    # if the label is equal to one of the two predictions, it returns 1 (correct), otherwise returns 0 (wrong)
    if label in emotion_predicted:
        accuracy_per_emotion[label][0] += 1
        accuracy_per_emotion[label][1] += 1
        return 1
    else:
        accuracy_per_emotion[label][1] += 1
        return 0

mean_accuracy = []
# ten iterations are performed in order to have always different training sets and test sets,
# for a greater evaluation of accuracy.
for number_split in range(NUMBER_IT):
    emotion_training_dictionary = {}
    test_subjects = []
    for key in emotion_dictionary:
        # mixed the subjects of each emotion
        random.shuffle(emotion_dictionary[key])
        subjects = emotion_dictionary[key]
        # training set is made up of 80 % of the subjects
        emotion_training_dictionary[key] = subjects[:int(len(subjects) * SPLIT_PERCENT)]
        # test set is made up of the remaining 20% of the subjects
        test_subjects.append(subjects[int(len(subjects) * SPLIT_PERCENT):])

    test_subjects = [item for sublist in test_subjects for item in sublist]

    # computation of the matrix of similarities between emotions
    for i in range(NUMBER_EMOTION):
        for j in range(NUMBER_EMOTION):
            df_weight[i + 1][j + 1] = get_emotion_similarities(i + 1, j + 1, DISTANCE_DIR)

    # extraction of average distances vectors of each emotion
    emotions_meanVector = {}
    for i in range(NUMBER_EMOTION):
        emotions_meanVector[i + 1] = mean_emotion_vector(emotion=i + 1, distance_dir=DISTANCE_DIR)

    # all the subjects of the test set are input and the accuracy is calculated
    accuracy_per_emotion = {}
    emotion_prediction_results = []
    for s in test_subjects:
        emotion_prediction_results.append(emotion_prediction(emotions_mean_vector=emotions_meanVector,
                                                             test_sub=s, distance_dir=DISTANCE_DIR))

    success = emotion_prediction_results.count(1)
    accuracy = (success / len(emotion_prediction_results)) * 100
    print(
        "N_SPLIT: {}, ACCURACY: {} - {}/{}".format(number_split, accuracy, success, len(emotion_prediction_results)))
    print("EMOTIONS_SUCCESS: ", accuracy_per_emotion)
    mean_accuracy.append(accuracy)

# the final accuracy is given by the average of the accuracies in the ten iterations
print("\nESEGUITE {} ITERAZIONI, L'ACCURATEZZA RISULTANTE È: {}".format(NUMBER_IT, statistics.mean(mean_accuracy)))
