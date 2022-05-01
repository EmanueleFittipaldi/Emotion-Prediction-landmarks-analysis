import os
import csv
import pandas as pd
from scipy import spatial
path_fcsv = "frames_csv"
path_globaldcsv = "global_distances_csv"

if not os.path.exists(path_globaldcsv):
    os.mkdir(path_globaldcsv)

for file in os.listdir(path_fcsv):
    if file.startswith("."): continue
    csv_name = file[0:4] + "_" + file[5:8] + "_GlobalDistances.csv"
    path_file = os.path.join(path_globaldcsv, csv_name)
    if not os.path.exists(path_file):
        # creazione file csv per la singola immagine
        f = open(path_file, 'w')
        # creazione del writer per scrivere le righe nel csv
        writer = csv.writer(f)
        firstEmptyRow = [0]*468
        # scrittura di tutte le righe nel csv
        writer.writerow(firstEmptyRow)
        f.close()

for file in os.listdir(path_globaldcsv)[:1]:
    filename = file[0:4] + "_" + file[5:8]
    frameToAnalyze = []
    for f in os.listdir(path_fcsv):
        if f.find(filename) != -1:
            frameToAnalyze.append(os.path.join(path_fcsv,f))
    frameToAnalyze = sorted(frameToAnalyze)
    first_csv = pd.read_csv(frameToAnalyze[0])
    print(first_csv)
    for csv in frameToAnalyze[1:]:
        print(csv)
        current_csv = pd.read_csv(csv)
        for i in range(len(first_csv)):
            # distance = spatial.distance.euclidean(
            #     [first_csv.at[i, 'x'], first_csv.at[i, 'y'], first_csv.at[i, 'z']],
            #     [current_csv.at[i, 'x'], current_csv.at[i, 'y'], current_csv.at[i, 'z']])
            print(list(first_csv.iloc[i]))
            print(list(current_csv.iloc[i]))


