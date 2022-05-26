import json
from utils import *

# Gathering all the csv containing local distances computed using euclidean and manhattan metric into two separate lists.
Local_Distances_euclidean = ["Local_Distances/" + x for x in os.listdir("Local_Distances/") if "euclidean.csv" in x]
Local_Distances_manhattan = ["Local_Distances/" + x for x in os.listdir("Local_Distances/") if "manhattan.csv" in x]

# ALPHA: Threshold by which we estabilish if there is any statistical significance difference between two populations
# MAX_FRAMES: Since micro-expressions are characterized by being faint and poor lasting, we expect them to happen only
# in the very first frames of a videose quence. For that reason we only consider the first 6 frames of a video sequence
# in order to detect a micro movement.
ALPHA = 0.05
MAX_FRAMES = 6

def get_statistical_significance():
    """
                    This function extracts all the meaningful landmarks using a test called two-tailed significance test.
                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
        """
    subjects_split_history = {}
    for path in sorted(Local_Distances_euclidean):

        videoSequence = pd.read_csv(path, header=None)
        splits = list(range(2, len(videoSequence) - 1))

        LandmarksPerSplit = {}
        for split in splits:
            landmarkSignificativi = []
            df_1 = videoSequence.iloc[:split, :]
            df_2 = videoSequence.iloc[split:, :]
            for i in range(0, 467):
                bool, significant = pvalue_test(vec1=df_1[i], vec2=df_2[i], alphaValue=ALPHA)
                if bool:
                    landmarkSignificativi.append(i)
            LandmarksPerSplit[split] = landmarkSignificativi

        maxValue = 0; split = 0; key_list = list(LandmarksPerSplit); size_list = 0
        if len(key_list) > MAX_FRAMES:
            size_list = MAX_FRAMES
        else:
            size_list = len(key_list)

        for i in range(1, size_list):
            key1 = key_list[i - 1]
            key2 = key_list[i]
            diff = (len(LandmarksPerSplit[key2]) - len(LandmarksPerSplit[key1]))
            if diff > maxValue:
                maxValue = diff
                split = key2
        if maxValue == 0 and split == 0:
            subjects_split_history[path[16:24]] = [[1, 2, 3], LandmarksPerSplit[2]]
        else:
            subjects_split_history[path[16:24]] = [[split - 1, split, split + 1], LandmarksPerSplit[split]]

            with open('subjects_significative_frame.json', 'w') as convert_file:
                convert_file.write(json.dumps(subjects_split_history))

def max_occurences_frame():
    """
                    funzione che visualizza le massime occorrenze di frame per ogni emozione.

                   - **Returns**:
                   - **Value return** has type
                   - Parameter **values**:
                   - **Precondition**:
        """
    emotion_directory = subjects_per_emotion(Dataset_Emotion=get_directories("Dataset/Emotion"), distance_name="_GD_euclidean")

    dic_mode = {}
    for key in sorted(emotion_directory):
        if key == 0: continue
        for sub in emotion_directory[key]:
            if key in dic_mode:
                dic_mode[key].append(str(data[sub[:8]][0]))
            else:
                dic_mode[key] = [str(data[sub[:8]][0])]

    for key in dic_mode:
        print("Emozione {}, numero di occorrenze maggiore: {}".format(key, statistics.mode(dic_mode[key])))


get_statistical_significance()

with open('subjects_significative_frame.json') as json_file:
    data = json.load(json_file)

# plot_results(data)
# max_occurences_frame()
