import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import numpy as np

# Carico il csv contenente le distanze di una sequenza video da analizzare
videoSequence = pd.read_csv("/Users/emanuelefittipaldi/PycharmProjects/Emotion_Prediction_Project/src/Local_Distances/S011_005_LD_manhattan.csv")

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
Pvalue_history=[]
splits = list(range(2,len(videoSequence)-1))
for split in splits:
    # split del dataset
    df_1 = videoSequence.iloc[:split, :]
    df_2 = videoSequence.iloc[split:, :]
    res = ttest_ind(df_1["0"],df_2["0"]).pvalue # questa è la funzione che presi i due insiemi di dati mi restituisce il pvalue
    Pvalue_history.append(res)

print(Pvalue_history)
for i in range(0,len(Pvalue_history)-1):
    print(Pvalue_history[i+1]-Pvalue_history[i])

# Le seguenti righe di codice sono soltanto per plottare a video il grafico della variazione del pvalue
x = np.array(splits)
y = np.array(Pvalue_history)
# plt.xlabel("splits")
plt.ylabel("pvalue")
plt.plot(x, y, color = "red", marker = "o", label = "pvalue")
plt.legend()
plt.show()