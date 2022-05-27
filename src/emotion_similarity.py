from utils import *

EMOTIONS = {1: "Anger",
            2: "Contempt",
            3: "Disgust",
            4: "Fear",
            5: "Happy",
            6: "Sadness",
            7: "Surprise"
            }
PATH_EMOTION = "Dataset/Emotion"
DATASET_EMOTION = get_directories(PATH_EMOTION)
DISTANCE_NAME = "_GD_euclidean"
DISTANCE_TYPEDIR = "Global_Distances/"
DISTANCES_FLAG = 1
LANDMARKS_FLAG = 0
EMOTIONS_NUMBER = 7
# dictionary that maintains the emotions with the different subjects,
# so the keys are the emotions and values all the subjects of that emotion
emotion_dictionary = subjects_per_emotion(dataset_emotion=DATASET_EMOTION, distance_name=DISTANCE_NAME)

def significative_values(flag_sign, distance_dir, emotion, emotion_subject):
    """
    This Function takes as input a directory that contains distances (euclidean or manhattan) and a list of subjects of an emotion.
    Opens the CSVs of the distances of each subject and calculates the threshold.
    Then obtain all the significant distances and landmarks, i.e. those that exceed this calculated threshold.
           - **Returns**: a dictionary in which key is a subject and values are distances or landmarks with directions.
           - **Value return** has type dict.
           - Parameter **values**: a flag that indicates if process landmarks or distances, directory of the distances,
                                    an emotion of the subjects and a list of subjects.
           - **Precondition**:
    """
    emotion_dict = {}

    for s in emotion_subject:
        frame_sequence = pd.read_csv(distance_dir + s, header=None)
        distances, sign_landmarks = process_threshold_landmarks(subject=s, emotion=emotion, frame_seq=frame_sequence)
        # if it is the flag on distances, then the significant distances are included in the diction,
        # otherwise the directions of each landmark are calculated
        # and a list of the type [landmark, x direction, y direction] is inserted in the dictionary
        if flag_sign == DISTANCES_FLAG:  # distances
            emotion_dict[s[:8]] = distances
        elif flag_sign == LANDMARKS_FLAG:  # landmarks
            directions = landmarks_XYdirections(subject=s[:8], index_frame=len(frame_sequence.axes[0]) - 1)
            for i in sign_landmarks:
                data = [i, directions[i][0], directions[i][1]]
                if s[:8] in emotion_dict:
                    emotion_dict[s[:8]].append(data)
                else:
                    emotion_dict[s[:8]] = [data]

    return emotion_dict


def get_emotion_similarities(flag_sign, emotion1, emotion2, distance_dir):
    """
     This Function takes as input two emotion key and a directory that contains distances.
        For each incoming emotion and for each subjects of an emotion, it extracts a distances list and calculates an average of similarities
        between these lists. The result is a percentage of similarity between two emotions.
        - **Returns**:
        - **Value return** has type
        - Parameter **values**:
        - **Precondition**:
           """
    # take all the subjects of emotion1 and emotion2 from dictionary of all emotions
    em1_subjects = emotion_dictionary[emotion1]
    em2_subjects = emotion_dictionary[emotion2]

    # dictionary that contains the vector of the distances of each subjects of emotion1 (same for emotion2)
    emotion1_sign = significative_values(flag_sign=flag_sign, distance_dir=distance_dir, emotion=EMOTIONS[emotion1], emotion_subject=em1_subjects)
    if emotion1 == emotion2:
        emotion2_sign = emotion1_sign
    else:
        emotion2_sign = significative_values(flag_sign=flag_sign, distance_dir=distance_dir,
                                             emotion=EMOTIONS[emotion2], emotion_subject=em2_subjects)

    # for each subject of emotion1 it calculates similarity with all the subjects of emotion2,
    # places the result in a list (all_similarities) and returns an average of all these similarities.
    all_similarities = []
    if flag_sign == DISTANCES_FLAG: # based on distances
        for key1 in emotion1_sign:
            for key2 in emotion2_sign:
                if key1 == key2: continue
                sim = vector_similarity(v1=emotion1_sign[key1], v2=emotion2_sign[key2])
                all_similarities.append(sim)
    elif flag_sign == LANDMARKS_FLAG: # based on landmarks and their directions
        for key1 in emotion1_sign:
            for key2 in emotion2_sign:
                if key1 == key2: continue
                # dictionary values are lists of lists([[l1, dx, d y], [l2, dx, dy], ...]),
                # so you need to create a single list of the type [l1, dx, dy, l2, dx, dy, ...]
                flat_em1 = [item for sublist in emotion1_sign[key1] for item in sublist]
                flat_em2 = [item for sublist in emotion2_sign[key2] for item in sublist]
                sim = vector_similarity(v1=flat_em1, v2=flat_em2)
                all_similarities.append(sim)

    return statistics.mean(all_similarities)


columns = { 1: [0, 0, 0, 0, 0, 0, 0],
            2: [0, 0, 0, 0, 0, 0, 0],
            3: [0, 0, 0, 0, 0, 0, 0],
            4: [0, 0, 0, 0, 0, 0, 0],
            5: [0, 0, 0, 0, 0, 0, 0],
            6: [0, 0, 0, 0, 0, 0, 0],
            7: [0, 0, 0, 0, 0, 0, 0],
            }
# matrix (7x7) that contains the percentage of similarities between all emotions based on distances
df_landmarks = pd.DataFrame(columns, index=[1, 2, 3, 4, 5, 6, 7])
df_landmarks = df_landmarks.astype(float)

# matrix (7x7) that contains the percentage of similarities between all emotions
# based on the landmarks and their directions on x-axis and y-axis
df_distances = pd.DataFrame(columns, index=[1, 2, 3, 4, 5, 6, 7])
df_distances = df_distances.astype(float)

for i in range(EMOTIONS_NUMBER):
    print("\n")
    for j in range(EMOTIONS_NUMBER):
        # distance-based similarity matrix calculation
        df_distances[i + 1][j + 1] = get_emotion_similarities(flag_sign=DISTANCES_FLAG, emotion1=i + 1,
                                                                                      emotion2=j + 1, distance_dir=DISTANCE_TYPEDIR)
        # similarity matrix calculation based on landmarks and their directions
        df_landmarks[i + 1][j + 1] = get_emotion_similarities(flag_sign=LANDMARKS_FLAG, emotion1=i + 1,
                                                              emotion2=j + 1, distance_dir=DISTANCE_TYPEDIR)

print("MATRICE SIM DISTANZE: \n", df_distances)
print("MATRICE SIM LANDMARK: \n", df_landmarks)

