from statistics import mode
import pandas as pd
from utils import *
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import operator

# Carico il csv contenente le distanze di una sequenza video da analizzare
videoSequence = pd.read_csv("Local_Distances/S999_003_LD_euclidean.csv", header=None)

# Pvalue_history: lista dei valori che il pvalue ha assunto per ciascun landmark e per ciascun split
# splitsChangeOccurred: lista dei frame in cui è avvenuta una variazione significativa di un landmark
# landmarksInvolved: lista dei landmark che hanno subito una variazione di posizione significativa all'interno della
# videosequenza
Pvalue_history = []
splitsChangeOccurred = []
landmarksInvolved = []
outlier = []


# lista di split per il quale voglio calcolare il pvalue
splits = list(range(1,len(videoSequence)-1))


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
delta = {}
for index_cutoff in splits:
    # index_cutoff = int(len(videoSequence.axes[0])/2)
    df_1 = videoSequence.iloc[1:index_cutoff+1, :468]
    df_2 = videoSequence.iloc[index_cutoff+1:, :468]
    df_1_concat = []
    df_2_concat = []
    for i in range(len(df_1.axes[0])):
        list = df_1.iloc[i:i+1, :].values.tolist()
        flat = [item for sublist in list for item in sublist]
        df_1_concat.append(flat)

    for i in range(len(df_2.axes[0])):
        list = df_2.iloc[i:i+1, :].values.tolist()
        flat = [item for sublist in list for item in sublist]
        df_2_concat.append(flat)

    flat_df_1 = [item for sublist in df_1_concat for item in sublist]
    flat_df_2 = [item for sublist in df_2_concat for item in sublist]

    delta[index_cutoff] = abs(statistics.mean(flat_df_2) - statistics.mean(flat_df_1))

    # significant = pvalueTest(flat_df_1, flat_df_2, alpha)

    # if significant[0]:
    #     print("STATISTICAL SIGNIFICANCE DETECTED")
    #     print("pvalue {}, split {}".format(significant[1], index_cutoff))
print(delta)
new_ma_val = max(delta.items(), key=operator.itemgetter(1))[0]
print("Media positivi: ",new_ma_val)

# for split in splits:
#
#     df_1 = videoSequence.iloc[:split, :]
#     df_2 = videoSequence.iloc[split:, :]
#     for i in range(0,467):
#         landmark = i
#         significant = pvalueTest(df_1[landmark],df_2[landmark],alpha)
#         if significant[0]:
#             # print("STATISTICAL SIGNIFICANCE DETECTED")
#             # print("pvalue{}, split{}, landmark{}".format(res,split,landmark))
#             splitsChangeOccurred.append(split)
#             landmarksInvolved.append(landmark)
#             Pvalue_history.append(significant[1])

# # STATS PRINTING
# print("\nThis is the frame where the major number of landmarks had a significant variation in the distance")
# print(mode(splitsChangeOccurred))
#
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
