import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statistics import mode
import numpy as np


def pvaluePlotter(Pvalue_history,splits):
    """
    This Function takes a list of pvalues and a list of splits where these pvalues where calculated and
    creates a plot showing how pvalue changed according to the several splits.
        - **Returns**: nothing

        - Parameter **Pvalue_history**: a list of pvalues

        - Parameter **splits**: a list of the split points where the pvalues where valuated

        - **Precondition**: Pvalue_history and splits are lists of numbers
    """
    x = np.array(splits)
    y = np.array(Pvalue_history)
    plt.ylabel("pvalue")
    plt.plot(x, y, color = "red", marker = "o", label = "pvalue")
    plt.legend()
    plt.show()
def histogramPlotter(data):
    plt.hist(data)
    plt.show()
def normalTest(values):
    """
    This function takes a list of numerical values and conduct a normal test over these values returning a p2 value.
    If this value is less than alpha, we conclude that the values were not drawn from a normal distribuition.

    - **Returns**: 1 if we can reject the null hypotesis, meaning that the values were not drawn from a normal distribuition,otherwise we return 0, meaning that the values were drawn from a normal distribuition.
    - **Value return** has type int.
    - Parameter **values**: the list of numerical values on which we want to conduct the normal test
    - **Precondition**: values is a list of numerical data

    """
    stat, p2 = stats.normaltest(values)
    alpha = 1e-3
    # print("p = {}".format(p2))
    if p2 < alpha:
        # the values were not drawn from a normal distribuition
        # print("the null hp can be rejected")
        return 1
    else:
        # the values were drawn from a normal distribuiton
        # print("the null hp cannot be rejected")
        return 0
def normalizeData(data):
    return np.log(data)
def pvalueTest(vec1,vec2,alphaValue):
    res = stats.ttest_ind(vec1,vec2).pvalue
    if res <= alphaValue:
        return True,res
    else:
        return False,res


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
# normlized = normalizeData(data)
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

