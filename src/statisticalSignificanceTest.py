from statistics import mode
import pandas as pd
from utils import *

# Carico il csv contenente le distanze di una sequenza video da analizzare
videoSequence = pd.read_csv("Local_Distances/S506_001_LD_euclidean.csv", header=None)

# Pvalue_history: lista dei valori che il pvalue ha assunto per ciascun landmark e per ciascun split
# splitsChangeOccurred: lista dei frame in cui è avvenuta una variazione significativa di un landmark
# landmarksInvolved: lista dei landmark che hanno subito una variazione di posizione significativa all'interno della
# videosequenza
Pvalue_history = []
splitsChangeOccurred = []
landmarksInvolved = []
outlier = []


# lista di split per il quale voglio calcolare il pvalue
splits = list(range(2,len(videoSequence)-1))


# Visualizzazione dell'istogramma delle distanze di un solo landmark prima e dopo la normalizzazione
# data = videoSequence.iloc[1:, :1]
# histogramPlotter(data)
# normalized = normalizeData(data)
# histogramPlotter(normalized)


for i in range(0,len(videoSequence.columns)-2):
    data = videoSequence.iloc[1:, i:i+1]
    videoSequence.iloc[1:, i:i+1] = abs(np.log(data))
    if normalTest(videoSequence.iloc[1:, i:i+1]):
        outlier.append(i)
print("Numero di landmark non normalizzati: {}, landmark: {}".format(len(outlier), outlier))

alpha = 0.01
for split in splits:
    df_1 = videoSequence.iloc[:split, :]
    df_2 = videoSequence.iloc[split:, :]
    for i in range(0,467):
        landmark = i
        significant = pvalueTest(df_1[landmark],df_2[landmark],alpha)
        if significant[0]:
            # print("STATISTICAL SIGNIFICANCE DETECTED")
            # print("pvalue{}, split{}, landmark{}".format(res,split,landmark))
            splitsChangeOccurred.append(split)
            landmarksInvolved.append(landmark)
            Pvalue_history.append(significant[1])

# STATS PRINTING
print("\nThis is the frame where the major number of landmarks had a significant variation in the distance")
print(mode(splitsChangeOccurred))

print("This is the list of the landmark involved in this emotion")
landmarksInvolved = set(landmarksInvolved)
landmarksInvolved = sorted(list(landmarksInvolved))
print(landmarksInvolved)
print(len(landmarksInvolved))

print("These are the key splits where major significance was detected")
splitsChangeOccurred =sorted(list(set(splitsChangeOccurred)))
print(splitsChangeOccurred)

