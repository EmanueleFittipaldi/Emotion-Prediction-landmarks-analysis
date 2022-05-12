from statistics import mode
import pandas as pd
from utils import *
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import operator
# Pvalue_history: lista dei valori che il pvalue ha assunto per ciascun landmark e per ciascun split
# splitsChangeOccurred: lista dei frame in cui è avvenuta una variazione significativa di un landmark
# landmarksInvolved: lista dei landmark che hanno subito una variazione di posizione significativa all'interno della
# videosequenza




Local_Distances_euclidean = ["Local_Distances/"+x for x in os.listdir("Local_Distances/") if "euclidean.csv" in x]
Local_Distances_manhattan = ["Local_Distances/"+x for x in os.listdir("Local_Distances/") if "manhattan.csv" in x]

# Visualizzazione dell'istogramma delle distanze di un solo landmark prima e dopo la normalizzazione
# data = videoSequence.iloc[1:, :1]
# histogramPlotter(data)
# normalized = normalizeData(data)
# histogramPlotter(normalized)


# Per ogni landmark, prendo tutti i valori della colonna, li normalizzo, li porto in valore assoluto e li
# memorizzo nella stessa colonna. Conduco poi il test di normalità per vedere se adesso tutte le misure per quel
# landmark segue una distribuzione normale. Se non la segue allora lo inserisco nella lista degli "outlier"
#
# for i in range(0,len(videoSequence.columns)-2):
#     data = videoSequence.iloc[1:, i:i+1]
#     videoSequence.iloc[1:, i:i+1] = abs(np.log(data))
#     if normalTest(videoSequence.iloc[1:, i:i+1]):
#         outlier.append(i)
# print("Numero di landmark non normalizzati: {}, landmark: {}".format(len(outlier), outlier))
alpha = 0.05
for path in Local_Distances_euclidean:
    videoSequence = pd.read_csv(path, header=None)
    splits = list(range(2, len(videoSequence) - 1))
    LandmarksPerSplit = {}
    for split in splits:
        landmarkSignificativi = []
        df_1 = videoSequence.iloc[:split, :]
        df_2 = videoSequence.iloc[split:, :]
        for i in range(0,467):
            landmark = i
            significant = pvalueTest(df_1[landmark],df_2[landmark],alpha)
            if significant[0]:
                landmarkSignificativi.append(landmark)
        LandmarksPerSplit[split] = landmarkSignificativi
    maxValue = 0

    for i in range(2,len(LandmarksPerSplit)):


    # print("Subject:{} #:{}, split:{}, landmarks:{}".format(path[16:24],len(landmarkSignificativi),split,landmarkSignificativi))
    # print("-----------------------------------------------")

# STATS PRINTING
# print("\nThis is the frame where the major number of landmarks had a significant variation in the distance")
# print(mode(splitsChangeOccurred))
#
# print("This is the list of the landmark involved in this emotion")
# landmarksInvolved = set(landmarksInvolved)
# landmarksInvolved = sorted(list(landmarksInvolved))
# print(landmarksInvolved)
# print(len(landmarksInvolved))
#
# print("These are the key splits where major significance was detected")
# splitsChangeOccurred =sorted(list(set(splitsChangeOccurred)))
# print(splitsChangeOccurred)
