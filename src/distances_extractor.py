import os
import csv
import pandas as pd
from scipy import spatial
from scipy.spatial import distance

# Path of the folder containing all the landmarks csv's for every videosequence
path_fcsv = "frames_csv"

def gloabl_distances(path_globaldcsv, namePath, nameDist):
    """
                  This function compute the global distances on every video sequence. These distances are
                  computed for every landmark, by comparing the position of the landmark in the first frame
                  to the position of the landmark in the frame i.

                  - **Returns**: nothing
                  - **Value return** has type: none
                  - Parameter **path_globaldcsv,namePath,nameDist**: String values representing the folder that will
                    contain the csv of the global distances for every video sequence, the name that these csv will have
                    and the choosen distance.
                  - **Precondition**: parameters must be string values. parameter nameDist must be 'EUCLIDEAN' or 'MANHATTAN'
       """
    listDistances = ['EUCLIDEAN', 'MANHATTAN']
    if nameDist in listDistances:
        if not os.path.exists(path_globaldcsv):
            os.mkdir(path_globaldcsv)

        # creating a csv for every emotion of every subject
        for file in os.listdir(path_fcsv):
            if file.startswith("."): continue

            # Making of the path in order to create the csv:
            # path format: SXXX_XXX_GD_(distance name).csv
            # SXXX identify the subject, XXX identify the emotion
            csv_name = file[0:4] + "_" + file[5:8] + "_" + namePath
            path_file = os.path.join(path_globaldcsv, csv_name)

            # checking if the csv doesn't already exist. if not, create the
            # csv with the first row containing all zeroes. These csv will follow this format:
            # every row is going to represent a different frame, and every column a different landmark.
            if not os.path.exists(path_file):
                firstEmptyRow = [0] * 468
                f = open(path_file, 'w')
                writer = csv.writer(f)
                writer.writerow(firstEmptyRow)
                f.close()

        # Up to this point we should have all the csv created and initialized.
        # We now have to fill them with the actual global distances.
        for file in os.listdir(path_globaldcsv):
            filename = file[0:4] + "_" + file[5:8]

            # This list is going to contain all the frames of a video sequence about a specific subject that
            # we have to analyze in order to extract the distances.
            frameToAnalyze = []
            for f in os.listdir(path_fcsv):
                if f.find(filename) != -1:
                    frameToAnalyze.append(os.path.join(path_fcsv,f))
            frameToAnalyze = sorted(frameToAnalyze)

            # In order to process the frames more easily, we open them as Dataframes. Since we are computing
            # global distances, we need to compare the position of all the landmarks in the frame interval 2-N
            # to the position of the landmarks in the first frame. So here I am reading the first frame.
            first_frame = pd.read_csv(frameToAnalyze[0])
            for data in frameToAnalyze[1:]:
                current_frame = pd.read_csv(data)
                distances = []
                for i in range(len(first_frame)):
                    if nameDist == "EUCLIDEAN":
                        dist = spatial.distance.euclidean(list(first_frame.iloc[i]), list(current_frame.iloc[i]))
                        distances.append(dist)
                    elif nameDist == "MANHATTAN":
                        dist = spatial.distance.cityblock(list(first_frame.iloc[i]), list(current_frame.iloc[i]))
                        distances.append(dist)

                # Once distances are computed, we open the csv previously initialized with zeroes
                # in order to fill them with the distances.
                path_csv = os.path.join(path_globaldcsv,data[11:20]+namePath)
                f = open(path_csv, "a")
                writer = csv.writer(f)
                writer.writerow(distances)
                f.close()
    else:
         print("Choose between computing Euclidean or Manhattan distances")

def local_distances(nameDist):
    """
                  This function compute the local distances on every video sequence. These distances are
                  computed for every landmark, by comparing the position of the landmark in the frame i-1
                  to the position of the landmark in the frame i.

                  - **Returns**: nothing
                  - **Value return** has type: none
                  - Parameter **nameDist**: String value representing the metric to use in order to compute distance
                    between landmarks.
                  - **Precondition**: parameter must be 'EUCLIDEAN' or 'MANHATTAN'
        """

    # Paths of the csv containing the landmark's position for every video sequence
    Csv_files = sorted(os.listdir(path_fcsv))

    # Creating and initializing a new csv for every subject. These csv will contain the distances
    # for every landmark from the i-1 frame to frame i.
    currentSubject = ""
    for frame in Csv_files:
        if currentSubject is not frame[0:9]:
            currentSubject = frame[0:9]
            filename = 'Local_Distances/' + frame[0:9] + 'LD' + '_' + nameDist+'.csv'
            f = open(filename, 'w')
            writer = csv.writer(f)
            FirstEmptyRow = [0] * 468
            writer.writerow(FirstEmptyRow)
            f.close()

    for VideoSequence in sorted(os.listdir("/Users/emanuelefittipaldi/PycharmProjects/Emotion_Prediction_Project/src/Local_Distances/")):

       # Since the Local_Distances folder may contain different csv for different metrics, I need to check
       # if I am opening the right csv.
       if nameDist in VideoSequence:
        LocalDistanceCSV = open("Local_Distances/" + VideoSequence, 'a')
        writer = csv.writer(LocalDistanceCSV)

        # For every Videosequnce about a subject I need to gather all the frames in order to analyze them
        frameToAnalyze = []
        for frame in Csv_files:
            if VideoSequence[0:8] in frame:
                frameToAnalyze.append(frame)


        i = 0
        j = 1

    # Computing the distances by taking the i-1 frame and i frame, and sliding this window
    # till the end of the videosequence
    while j < len(frameToAnalyze):
        rowOfDistances = []
        previousFrame= os.path.join("frames_csv/", frameToAnalyze[i])
        currentFrame= os.path.join("frames_csv/", frameToAnalyze[j])
        previousFrame_Df = pd.read_csv(previousFrame)
        currentFrame_Df = pd.read_csv(currentFrame)

        for k in range(previousFrame_Df.shape[0]):
            landmarkPrecedente = list(previousFrame_Df.iloc[k])
            landmarkCorrente = list(currentFrame_Df.iloc[k])

            if nameDist == "EUCLIDEAN":
                rowOfDistances.append(distance.euclidean(landmarkPrecedente, landmarkCorrente))
            elif nameDist == "MANHATTAN":
                rowOfDistances.append(distance.cityblock(landmarkPrecedente, landmarkCorrente))
            else:
                print("EUCLIDEAN or MANHATTAN only")
        writer.writerow(rowOfDistances)
        i += 1
        j += 1

    LocalDistanceCSV.close()


# FUNCTION CALLS TO RUN ONLY ONCE:

# Computing of global distances using Euclidean metric
# gloabl_distances("Global_Distances", "GD_euclidean.csv", "EUCLIDEAN")

# Computing of global distances using Manhattan metric
# gloabl_distances("GD_manhattan_csv", "GD_manhattan.csv", "MANHATTAN")

# Computing of local distances using Euclidean metric
# local_distances('EUCLIDEAN')

# Computing of local distances using Manhattan metric
# local_distances('MANHATTAN')