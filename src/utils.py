import os

import pandas as pd
from scipy import stats
import numpy as np
from matplotlib import pyplot as plt
from scipy import spatial
import statistics
import csv



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
    """
     This Function takes a list of values and uses np.log() function to normalize them. After the application of this
     function, all the data should now follow a normal distribuition.
         - **Returns**: list of normalized values

         - Parameter **data**: a list of numerical data


         - **Precondition**: Data must be a list of values
     """
    return np.log(data)


def pvalueTest(vec1, vec2, alphaValue):
    """
     This Function takes two lists of numerical values representing two hypotetically distinguished distribuitions of values,
     and an alpha value. Through pvalue we compare these two distribuitions, returning if they are statistically different.
         - **Returns**: True or False as a result of the statistical significance test and the pvalue
         - **Value return** has type boolean and float.
         - Parameter **vec1,vec2**: lists of numerical values
         - Parameter **alphaValue**: threshold by which we can conclude an example is significant or not
         - **Precondition**: vec1,vec2 lists of numerical values. alphavalue a single float number
     """
    res = stats.ttest_ind(vec1, vec2).pvalue
    if res <= alphaValue:
        return True, res
    else:
        return False, res


def getDirectories(path_dataset):
    """
     This Function takes as input the path of the Dataset and returns a list containing all the paths for the directories
     of each videosequence.
         - **Returns**: List of the videosequence directories paths.
         - **Value return**: List of strings.
         - Parameter **path_dataset**: path of the dataset, type string.
         - **Precondition**: Dataset must exists at path indicated. path_dataset type string
     """
    # struttura dati che contiene i path delle singole directory di ogni singolo soggetto
    Dataset_folders = []
    for root, subdirs, files in os.walk(path_dataset):
        for d in subdirs:
            # considero solo le sottocartelle dei singoli soggetti (iniziano con S)
            if (os.path.basename(d).startswith("S")):
                # path fino alle sottocartelle singole (001, 002, 003, etc.)
                path_sdir = os.path.join(path_dataset, d)
                for dir in os.listdir(path_sdir):
                    # escludo .DS_STORE e le cartelle nascoste
                    if (not dir.startswith(".")):
                        # salvataggio all'interno della struttura dati
                        Dataset_folders.append(os.path.join(path_sdir, dir))
    return Dataset_folders


# funzione per andare a calcolare le direzioni dei landmark su asse x e y
def landmarks_XYdirections(subject, indexF):
    path_dir = "frames_csv"
    frames = []
    for file in sorted(os.listdir(path_dir)):
        if file.startswith(subject):
            frames.append(os.path.join(path_dir, file))

    landmarks_directions = {}
    firstFrame = pd.read_csv(frames[0])
    lastFrame = pd.read_csv(frames[indexF])

    for i in range(468):
        directions = []
        coordXFirst = firstFrame['x'][i]
        coordXLast = lastFrame['x'][i]
        coordYFirst = firstFrame['y'][i]
        coordYLast = lastFrame['y'][i]

        if (coordXLast - coordXFirst) > 0:
            directions.append(+1)
        else:
            directions.append(-1)
        if (coordYLast - coordYFirst) > 0:
            directions.append(+1)
        else:
            directions.append(-1)

        landmarks_directions[i] = directions

    return landmarks_directions

def vectorSimilarity(v1, v2):
    """
      This Function takes as input two lists of numerical values and return in % how similiar they are using the spatial distance
      cosine.
          - **Returns**: float indicating the percentage of how similiare these two lists of values are.
          - **Value return**: % as a float number.
          - Parameter **v1,v2**: lists of numerical values.
          - **Precondition**:v1,v2 must be numerical values
      """
    if len(v1) > len(v2):
        delta = len(v1) - len(v2)
        for i in range(delta):
              # v2.append(statistics.mean(v2))
             v2.append(0)
    elif len(v1) < len(v2):
        delta = len(v2) - len(v1)
        for i in range(delta):
            # v1.append(statistics.mean(v1))
             v1.append(0)

    return 1 - spatial.distance.cosine(v1, v2)