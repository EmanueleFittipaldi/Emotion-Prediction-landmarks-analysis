import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statistics import mode
import numpy as np

def pvaluePlotter(pvalueHistory,splits):
    x = np.array(splits)
    y = np.array(Pvalue_history)
    plt.ylabel("pvalue")
    plt.plot(x, y, color = "red", marker = "o", label = "pvalue")
    plt.legend()
    plt.show()


def normalTest(values):
    stat, p2 = stats.normaltest(values)
    alpha = 1e-3
    # print("p = {}".format(p2))
    if p2 < alpha:
        # print("the null hp can be rejected")
        return 1
    else:
        # print("the null hp cannot be rejected")
        return 0


# Carico il csv contenente le distanze di una sequenza video da analizzare
videoSequence = pd.read_csv("Local_Distances/S506_001_LD_euclidean.csv", header=None)

# array contenente la variazione del pvalue in base al frame in cui mi trovo.
# es. tra il frame 2-3 il pvalue vale 0.80, tra il frame 3-4 il pvalue vale 0.30, etc ...
# l'ipotesi è che tra tutti questi pvalue ci sia un picco netto che dimostra una variazione significativa
# in termini di distanza per il landmark che stiamo considerando (in questo esempio sto misurando la significatività
# soltanto del landmark 0).
#
# Come calcolare il pvalue:
# Per poter calcolare il pvalue devo avere due insiemi di dati che io considero differenti. Nel nostro caso
# l'ipotesi è che i valori delle distanze di un landmark, fino ad un certo punto appartengono ad una microespressione
# ma da un certo punto in poi (che vogliamo scoprire) appartengono alla distribuzione di dati di una macroespressione.
# devo quindi dividere il dataframe delle distanze in due fette orizzontalmente, dove la prima fetta sono i valori
# che io dico appartenere alla microespressione mentre la seconda fetta contiene i valori che io dico appartenere
# alla macroespressione. Dato che io non conosco effettivamente dov'è questo punto, ovvero dove la microespressione
# diventa macroespressione, devo provare a "tagliare" il dataset provando diversi split. Per es. se la mia videosequenza
# è composta da 10 frame, allora provo prima a dire che: "i primi 2 frame sono microespressione e i successivi 8" sono
# macroespressione, calcolo il pvalue e lo memorizzo in Pvalue_history. Faccio questa cosa fino a quando non splitto
# il dataframe in len-2 frame di microespressione e 2 frame di macroespressione. L'ipotesi è che quando il pvalue raggiunge
# un picco per la prima volta allora siamo passati da micro a macro-espressione.
Pvalue_history = [] # lista dei valori che il pvalue ha assunto per ciascun landmark e per ciascun split
splitsChangeOccurred = [] # lista dei frame in cui è avvenuta una variazione significativa di un landmark
landmarksInvolved = [] # lista dei landmark che hanno subito una variazione di posizione significativa all'interno della videosequenza

splits = list(range(2,len(videoSequence)-1))
# Regolare questo valore tra 0.05 e 0.01 per incrementare oppure decrementare la soglia per la quale decretiamo
# la variazione di posizione di un landmark come significativa oppure no. Mettendo una soglia molto bassa come 0.01
# otteniamo i landmark che più rappresentativamente hanno oltrepassato la soglia alpha.

# Grafici per visualizzare l'andamento dei dati dopo averli normalizzati
# data = videoSequence.iloc[1:, :1]
# plt.hist(data)
# plt.show()
# plt.hist(np.log(data))
# plt.show()

print(videoSequence)
# Per poter applicare il test di significatività su ciascun landmark abbiamo bisogno che le distanze registrate seguino
# una distribuzione normale (gaussiana) altrimenti non è possibile applicarlo.
# senza la normalizzazione abbiamo riscontrato in media 150 landmark che non seguivano una distribuzione normale.
# dopo la trasformazione abbiamo ridotto il numero a circa 20 landmark, non è possibile migliorarlo
# poiché le distanze registrate non sono di un numero sufficientemente ampie
# plt.hist(videoSequence.iloc[1:, 3:4])
# plt.show()
outlier = []
for i in range(0,len(videoSequence.columns)-2):
    data = videoSequence.iloc[1:, i:i+1]
    videoSequence.iloc[1:, i:i+1] = abs(np.log(data))
    if normalTest(videoSequence.iloc[1:, i:i+1]):
        outlier.append(i)
print("Numero di landmark non normalizzati: {}, landmark: {}".format(len(outlier), outlier))
# plt.hist(videoSequence.iloc[1:, 3:4])
# plt.show()

print(videoSequence)


alpha = 0.01

for split in splits:
    df_1 = videoSequence.iloc[:split, :]
    df_2 = videoSequence.iloc[split:, :]
    for i in range(0,467):
        landmark = i
        res = stats.ttest_ind(df_1[landmark],df_2[landmark]).pvalue
        if res <= alpha:
            # print("STATISTICAL SIGNIFICANCE DETECTED")
            # print("pvalue{}, split{}, landmark{}".format(res,split,landmark))
            splitsChangeOccurred.append(split)
            landmarksInvolved.append(landmark)
            Pvalue_history.append(res)

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

