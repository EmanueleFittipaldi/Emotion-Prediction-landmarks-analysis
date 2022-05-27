import json
from utils import *

# Gathering all the csv containing local distances computed using euclidean and manhattan metric into two separate lists.
Local_Distances_euclidean = ["Local_Distances/" + x for x in os.listdir("Local_Distances/") if "euclidean.csv" in x]
Local_Distances_manhattan = ["Local_Distances/" + x for x in os.listdir("Local_Distances/") if "manhattan.csv" in x]

# ALPHA: Threshold by which we estabilish if there is any statistical significance difference between two populations
# MAX_FRAMES: Since micro-expressions are characterized by being faint and poor lasting, we expect them to happen only
# in the very first frames of a videose quence. For that reason we only consider the first 6 frames of a video sequence
ALPHA = 0.05
MAX_FRAMES = 6

def get_statistical_significance():
    """
         This function writes a json containing all the subjects with the frame interval where the micro-expression
         was detected and the list of all the landmarks involved into that action.

    """

    subjects_split_history = {}
    for path in sorted(Local_Distances_euclidean):

        # For every videoSequence we have to compare two populations of local distances in order
        # to estabilish if there is any statistical significant difference between the two. If that's the case
        # we know that a landmark has moved in a meaningful manner so we keep track of them using
        # landmarkSignificativi list. Since we don't know who these populations are, we have
        # to check every possible split between local distances measurements until we find the pair of populations
        # that gives us a statistical significance.
        videoSequence = pd.read_csv(path, header=None)
        splits = list(range(2, len(videoSequence) - 1))

        # These structure keeps track of the statistical relevant landmarks for every split tried.
        LandmarksPerSplit = {}

        for split in splits:
            landmarkSignificativi = []
            df_1 = videoSequence.iloc[:split, :] # Population 1
            df_2 = videoSequence.iloc[split:, :] # Population 2

            # For every landmark we conduct two-tailed pvalue test. If True is returned
            # the landmark is needed to be saved since it is relevant.
            for i in range(0, 467):
                bool, significant = pvalue_test(vec1=df_1[i], vec2=df_2[i], alphaValue=ALPHA)
                if bool:
                    landmarkSignificativi.append(i)
            LandmarksPerSplit[split] = landmarkSignificativi

        # Through landmarkPerSplit we now have a description of the video sequence in terms of statistical
        # significant landmarks per frame. In order to detect where the micro-expression happend we have to
        # check between which frames there was a huge increase of meaningful landmarks. In order to accomplish that
        # we computed the Delta between the number of meaningful landmarks in frame i and i-1. We then took
        # the split where Delta is max.

        maxValue = 0; split = 0; key_list = list(LandmarksPerSplit); size_list = 0

        # Here we apply the hypotesis by which micro-expressions are faint and poor lasting. It is of no use
        # checking for micro-expressions in the last frames so we take just the first 6 frames if the video sequence
        # last more than 6 frames or we take all the frames if video sequence is less or equal than 6 frames
        if len(key_list) > MAX_FRAMES:
            size_list = MAX_FRAMES
        else:
            size_list = len(key_list)

        for i in range(1, size_list):
            key1 = key_list[i - 1]
            key2 = key_list[i]
            diff = (len(LandmarksPerSplit[key2]) - len(LandmarksPerSplit[key1])) # computing the Delta
            if diff > maxValue:
                maxValue = diff
                split = key2
        if maxValue == 0 and split == 0:
            subjects_split_history[path[16:24]] = [[1, 2, 3], LandmarksPerSplit[2]]
        else:
            # We return a neighborhood of the frame in which a micro-expression is detected. We find more
            # logical doing so since a micro-expression is something that lasts at least three frames.
            subjects_split_history[path[16:24]] = [[split - 1, split, split + 1], LandmarksPerSplit[split]]

            # We save all the results into a .json
            with open('micro-expression_results/subjects_significative_frame.json', 'w') as convert_file:
                convert_file.write(json.dumps(subjects_split_history))

def max_occurences_frame(data):
    """
                    This function takes into consideration for every emotion, all the frame intervals where a micro-expression
                    was detected. Since this interval is different from subject to subject, this function counts the occurrencies
                    of every interval and prints the max value.
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

# ----------------------------------------------------------------------------------------------------------------------
# CODE TO BE RUNNED ONLY ONCE

# get_statistical_significance()
# with open('micro-expression_results/subjects_significative_frame.json') as json_file:
#     data = json.load(json_file)
# plot_results(data)
# max_occurences_frame(data)
