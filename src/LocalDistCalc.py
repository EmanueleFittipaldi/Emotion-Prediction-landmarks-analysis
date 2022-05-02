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
    if currentSubject is not frame[0:9]:  # ogni volta che la sequenza o il soggetto cambia creo un nuovo csv
        currentSubject = frame[0:9]

        # Creo il nuovo csv
        # filename = 'Local_Distances/' + frame[0:9] + 'LocalDistances.csv' per creare i file contenenti le distanze EUCLIDEE
        filename = 'manhattan/'+frame[0:9]+'LD_manhattan.csv'
        f = open(filename, 'w')
        writer = csv.writer(f)

        # Scrivo la prima riga delle distanze che sarà composta da
        # 468 valori uguali a 0
        FirstEmptyRow = [0] * 468
        writer.writerow(FirstEmptyRow)
        f.close()

# Per ogni csv di distanze locali devo analizzare tutti i frame di
# quella sequenza e devo scrivere i risultati in quel csv
# for VideoSequence in sorted(os.listdir(hp.getFromEnv('Local_Distances'))):
for VideoSequence in sorted(os.listdir("/Users/emanuelefittipaldi/PycharmProjects/Emotion_Prediction_Project/src/manhattan")):
    #LocalDistanceCSV = open("Local_Distances/"+VideoSequence,'a')
    LocalDistanceCSV = open("manhattan/" + VideoSequence, 'a')
    writer = csv.writer(LocalDistanceCSV)

    # lista contenente i nomi dei frame appartenenti alla sequenza video
    # per reperirli scorro tutti i nomi dei frame
    frameToAnalyze = []
    for frame in Csv_files:
        if VideoSequence[0:8] in frame:
            frameToAnalyze.append(frame)


    # adesso ho tutti frame per quella sequenza, e li apro come dataframe
    i = 0
    j = 1

    while j < len(frameToAnalyze):
        rowOfDistances = []
        previousFrame= os.path.join("frames_csv/", frameToAnalyze[i])
        currentFrame= os.path.join("frames_csv/", frameToAnalyze[j])
        previousFrame_Df = pd.read_csv(previousFrame)
        currentFrame_Df = pd.read_csv(currentFrame)

        # devo scorrere le righe di entrambi i csv, calcolare la distanza
        # con la libreria di scipy e scrivere il risultato in una colonna
        # del csv delle distanze locali

        for k in range(previousFrame_Df.shape[0]):
            landmarkPrecedente = list(previousFrame_Df.iloc[k])
            landmarkCorrente = list(currentFrame_Df.iloc[k])
            # rowOfDistances.append(distance.euclidean(landmarkPrecedente,landmarkCorrente))
            rowOfDistances.append(distance.cityblock(landmarkPrecedente, landmarkCorrente))
        writer.writerow(rowOfDistances)
        i+=1
        j+=1

    LocalDistanceCSV.close()























