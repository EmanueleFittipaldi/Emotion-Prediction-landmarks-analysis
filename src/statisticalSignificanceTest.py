import json
import pandas as pd
from utils import *

Local_Distances_euclidean = ["Local_Distances/"+x for x in os.listdir("Local_Distances/") if "euclidean.csv" in x]
Local_Distances_manhattan = ["Local_Distances/"+x for x in os.listdir("Local_Distances/") if "manhattan.csv" in x]

subjects_split_history = {}
alpha = 0.05
for path in sorted(Local_Distances_euclidean):
    videoSequence = pd.read_csv(path, header=None)
    splits = list(range(2, len(videoSequence) - 1))
    LandmarksPerSplit = {}
    for split in splits:
        landmarkSignificativi = []
        df_1 = videoSequence.iloc[:split, :]
        df_2 = videoSequence.iloc[split:, :]
        for i in range(0,467):
            landmark = i
            significant = pvalueTest(df_1[landmark], df_2[landmark], alpha)
            if significant[0]:
                landmarkSignificativi.append(landmark)
        LandmarksPerSplit[split] = landmarkSignificativi

    maxValue = 0
    split = 0
    key_list = list(LandmarksPerSplit)
    for i in range(1, len(key_list)):
        key1 = key_list[i-1]
        key2 = key_list[i]
        diff = (len(LandmarksPerSplit[key2]) - len(LandmarksPerSplit[key1]))
        # if len(LandmarksPerSplit[key1]) > len(LandmarksPerSplit[key2]) and key1 == 2:
        #     maxValue = abs(diff)
        #     split = key1
        #     break
        if diff > maxValue:
            maxValue = diff
            split = key2
    if maxValue == 0 and split == 0:
        subjects_split_history[path[16:24]] = [[1, 2, 3], LandmarksPerSplit[2]]
    else:
        print("Subject: {}, split: {}".format(path[16:24], split))
        print("Subject: {}, split: {}, landmarks: {}, #: {}".format(path[16:24], [split - 1, split, split + 1],
                                                                LandmarksPerSplit[split],
                                                                len(LandmarksPerSplit[split])))

        subjects_split_history[path[16:24]] = [[split - 1, split, split + 1], LandmarksPerSplit[split]]

print(subjects_split_history)

with open('subjects_significative_frame.json', 'w') as convert_file:
    convert_file.write(json.dumps(subjects_split_history))
