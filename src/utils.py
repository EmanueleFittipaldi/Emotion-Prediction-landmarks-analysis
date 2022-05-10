import os
from scipy import stats
import numpy as np
from matplotlib import pyplot as plt
from scipy import spatial
import statistics

def pvaluePlotter(Pvalue_history, splits):
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
    plt.plot(x, y, color="red", marker="o", label="pvalue")
    plt.legend()
    plt.show()


def histogramPlotter(data):
    """
     This Function takes a list of values and uses plt.hist() to plot them
         - **Returns**: nothing

         - Parameter **data**: a list of pvalues


         - **Precondition**: list of values
     """
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
             v2.append(statistics.mean(v2))
            # v2.append(0)
    elif len(v1) < len(v2):
        delta = len(v2) - len(v1)
        for i in range(delta):
            v1.append(statistics.mean(v1))
            # v1.append(0)

    return 1 - spatial.distance.cosine(v1, v2)
