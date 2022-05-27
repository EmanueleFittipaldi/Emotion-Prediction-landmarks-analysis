import os
import pandas as pd
from scipy import stats, spatial
import statistics
import cv2
import mediap_util as mpu
import csv

def extract_landmarks(dir,img):
    """
       This Function takes in input the path of directory and image included in this directory,
       extracts 468 landmarks and places the micro-expression_results in a csv file.
          - **Returns**: null.
          - **Value return** has type null.
          - Parameter **values**: path of directory, image
          - **Precondition**: dir type string, path of the image
       """
    filename = ('frames_csv/'+str(img)).replace('.png', '.csv')
    file = open(filename, 'w')
    writer = csv.writer(file)
    writer.writerow(['x','y','z'])

    image = cv2.imread(os.path.join(dir, img))
    num_faces, keypoints = mpu.TESS(image)

    # struttura dati che contiene i landmark divisi per righe (468x3)
    data = []
    for row in keypoints:
        data.append(row)
    writer.writerows(data)
    file.close()

def pvalue_test(vec1, vec2, alphaValue):
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

def get_directories(path_dataset):
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

def landmarks_XYdirections(subject, indexFrame):
    """
     This function takes as input a person and a frame index of interest from which to obtain the distances and calculate
     the directions on the x and y axes of the landmarks with respect to the first frame.
    Give +1 if it's the same direction, -1 otherwise.
         - **Returns**: list of landmarks directions.
         - **Value return** has type list.
         - Parameter **path_dataset**: subject, frame index of interest
         - **Precondition**: subject type string and in the form: "SXXX_XXX", indexFrame type integer.
     """
    path_dir = "frames_csv/"

    frames = [path_dir + x for x in sorted(os.listdir(path_dir)) if subject in x]

    landmarks_directions = {}
    firstFrame = pd.read_csv(frames[0])
    lastFrame = pd.read_csv(frames[indexFrame])

    for i in range(468):
        directions = []
        if (lastFrame['x'][i] - firstFrame['x'][i]) > 0:
            directions.append(+1)
        else:
            directions.append(-1)
        if (lastFrame['y'][i] - firstFrame['y'][i]) > 0:
            directions.append(+1)
        else:
            directions.append(-1)

        landmarks_directions[i] = directions

    return landmarks_directions

def vector_similarity(v1, v2):
    """
      This Function takes as input two lists of numerical values and return in % how similiar they are using the spatial distance
      cosine.
          - **Returns**: float indicating the percentage of how similiare these two lists of values are.
          - **Value return**: % as a float number.
          - Parameter **v1,v2**: lists of numerical values.
          - **Precondition**:v1,v2 must be numerical values
      """
    if len(v1) > len(v2):
        while len(v2) < len(v1):
            v2.append(0)
    elif len(v1) < len(v2):
        while len(v1) < len(v2):
            v1.append(0)

    return 1 - spatial.distance.cosine(v1, v2)

def subjects_per_emotion(Dataset_Emotion, distance_name):
    """
    This Function takes as input a emotions dataset and distance name (to get the CSV files of the distance of interest),
    creates a dictionary in which the keys are the emotions and the values are the subjects of that key emotion.
             - **Returns**: dictionary that contains subjects divided by emotions.
             - **Value return**: dictionary.
             - Parameter **path_dataset**: emotions dataset, distance name of interest.
             - **Precondition**: distance name type string.
         """
    emotion_dictionary = {}
    for dir in Dataset_Emotion:
        for file in os.listdir(dir):
            if os.path.basename(file).find('emotion') != -1:
                subject = file[:8] + distance_name + ".csv"
                filename = os.path.join(dir, file)
                f = open(filename, "r")
                string_formatted = float(f.read().strip())
                f.close()
                if string_formatted in emotion_dictionary:
                    emotion_dictionary[string_formatted].append(subject)
                else:
                    emotion_dictionary[string_formatted] = [subject]
    return emotion_dictionary

def get_distances_overT(frame, threshold):
    """
    This Function takes as input a frame of interest and a threshold, checks for each landmark of the frame if its distance
    is a greater than the threshold, this mean that the landmark is significant and its distance and a number are inserted in a list (corresponds to the landmark).
       - **Returns**: two list: a list of all significant distances and a list of all significant landmarks.
       - **Value return** has type list, list
       - Parameter **values**: frame of interest, is a pandas dataframe, threshold a float.
       - **Precondition**: frame of interest must be a dataframe.
       """
    distances_overT = []
    landmarks = []
    for i in range(0,468):
        if frame[i] > threshold:
            distances_overT.append(frame[i])
            landmarks.append(i)
    return distances_overT, landmarks

def process_threshold_landmarks(subject, emotion, frameSeq):
    """
    This Function takes as input a sequence of frames of the subject of interest, and calculate a threshold.
    The threshold is the average of the differences between the distances.
          - **Returns**:
          - **Value return** has type
          - Parameter **values**:
          - **Precondition**:
       """
    number_rows = len(frameSeq.axes[0])

    dist_ff = frameSeq.iloc[1:2, :468].values.tolist()
    fldist_ff = [item for sublist in dist_ff for item in sublist]

    dist_lf = frameSeq.iloc[number_rows-1:number_rows, :468].values.tolist()
    fldist_lf = [item for sublist in dist_lf for item in sublist]

    delta_distances = []
    for i in range(0, 468):
        delta = fldist_lf[i] - fldist_ff[i]
        delta_distances.append(delta)

    threshold = statistics.mean(delta_distances)

    distancesOverT, significativeLandmarks = get_distances_overT(fldist_lf, threshold)

    # plot a histogram or a 3D graph to visualize significant landmarks
    # plot.plot_significative_landmarks('Global Distances', subject, frameSeq, distancesOverT, significativeLandmarks)
    # plot.plot_scatter3D(subject[:8], emotion, significativeLandmarks)

    return distancesOverT, significativeLandmarks