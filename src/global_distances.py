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
    emotion_dir = []
    for f in os.listdir(path_fcsv):
        if f.find(filename) != -1:
            emotion_dir.append(os.path.join(path_fcsv,f))
    emotion_dir = sorted(emotion_dir)
    first_csv = pd.read_csv(emotion_dir[0])
    for csv in emotion_dir[1:]:
        current_csv = pd.read_csv(csv)
        for i in range(len(first_csv)):
            distance = spatial.distance.seuclidean(
                [first_csv.at[i, 'x'], first_csv.at[i, 'y'], first_csv.at[i, 'z']],
                [current_csv.at[i, 'x'], current_csv.at[i, 'y'], current_csv.at[i, 'z']],
                [0.1, 0.1, 0.1])
            print(distance)


