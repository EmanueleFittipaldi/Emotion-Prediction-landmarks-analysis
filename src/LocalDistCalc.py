import os
import Helper as hp
import csv
import pandas as pd
from scipy.spatial import distance

# Reperisco il path della cartella dove sono memorizzati
# tutti i csv contenenti i landmarks
path_csv = hp.getFromEnv('CsvPath')
Csv_files = sorted(os.listdir(path_csv))



# Creo all'interno di una cartella chiamata Local_Distances
# dei csv rappresentanti le distanze locali per sequenza video
# dei landmarks. Questi csv sono tali che la prima riga è sempre composta da 468 colonne poste a 0
currentSubject = ""
for frame in Csv_files:
    if currentSubject is not frame[0:9]: #ogni volta che la sequenza o il soggetto cambia creo un nuovo csv
        currentSubject = frame[0:9]

        # Creo il nuovo csv e.g. Local_Distance/S005_001_LocalDistances.csv
        filename = 'Local_Distances/'+frame[0:9]+'LocalDistances.csv'
        f = open(filename, 'w')
        writer = csv.writer(f)

        # Scrivo la prima riga delle distanze che sarà composta da
        # 468 valori uguali a 0
        FirstEmptyRow = [0] * 468
        writer.writerow(FirstEmptyRow)
        f.close()

# Per ogni csv di distanze locali devo analizzare tutti i frame di
# quella sequenza e devo scrivere i risultati in quel csv
for VideoSequence in sorted(os.listdir(hp.getFromEnv('Local_Distances'))):
    df = pd.read_csv("Local_Distances/"+VideoSequence) #apro il csv in un dataframe

    # lista contenente i nomi dei frame appartenenti alla sequenza video
    # per reperirli scorro tutti i nomi dei frame
    frameToAnalyze = []
    for frame in Csv_files:
        if VideoSequence[0:8] in frame:
            frameToAnalyze.append(frame)

    # adesso ho tutti frame per quella sequenza, e li apro come dataframe
    # Nota: li apro se contengono qualcosa altrimenti avrei un errore.
    framePath= os.path.join("frames_csv/",frameToAnalyze[0])
    if os.path.getsize(framePath) !=0:
          df1 = pd.read_csv(framePath)
    else:
        continue

    # df2 = pd.read_csv(os.path.join("frames_csv/", frameToAnalyze[1]))
    # print(df1)























