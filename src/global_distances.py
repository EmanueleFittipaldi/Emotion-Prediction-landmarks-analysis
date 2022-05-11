import os
import csv
import pandas as pd
from scipy import spatial

# calcolo delle ditanze globali per ogni sequenza video
# la distanza globale è calcolata su ogni frame rispetto al primo della sequenza
path_fcsv = "frames_csv"

def distance_calc(path_globaldcsv, namePath, nameDist):
    listDistances = ['EUCLIDEAN', 'MANHATTAN']
    if nameDist in listDistances:
        # creazione cartella principale inerente alla distanza richiesta se non esiste già
        if not os.path.exists(path_globaldcsv):
            os.mkdir(path_globaldcsv)
        # loop per creare csv per ogni emozione di ogni soggeto
        for file in os.listdir(path_fcsv):
            if file.startswith("."): continue
            # path formato da: SXXX_XXX_GD_(nome distanza).csv
            # SXXX rappresenta il soggetto, XXX rappresenta l'emozione
            csv_name = file[0:4] + "_" + file[5:8] + "_" + namePath
            # path completo con directory
            path_file = os.path.join(path_globaldcsv, csv_name)
            # se il csv non esiste viene creato e aggiunta la prima riga con tutte le distanze a 0
            if not os.path.exists(path_file):
                firstEmptyRow = [0] * 468
                f = open(path_file, 'w')
                writer = csv.writer(f)
                writer.writerow(firstEmptyRow)
                f.close()

        # loop per prendere i singoli csv creati, inserendo all'interno le distanze calcolate
        for file in os.listdir(path_globaldcsv):
            # path formato da: SXXX_XXX_GD_(nome distanza).csv
            # SXXX rappresenta il soggetto, XXX rappresenta l'emozione
            filename = file[0:4] + "_" + file[5:8]
            # struttura dati che contiene i frame da analizzare di ogni sequenza video divise per soggetto ed emozione
            frameToAnalyze = []
            # verifico se il frame corrente corrisponde all'emozione XXX del sogetto SXXX (del filename)
            for f in os.listdir(path_fcsv):
                if f.find(filename) != -1:
                    # viene aggiunto tra i frame da analizzare
                    frameToAnalyze.append(os.path.join(path_fcsv,f))
            frameToAnalyze = sorted(frameToAnalyze)
            # costruzione DataFrame del primo frame
            first_frame = pd.read_csv(frameToAnalyze[0])
            # loop sui frame successivi al primo
            for data in frameToAnalyze[1:]:
                current_frame = pd.read_csv(data)
                distances = []
                # calcolo delle distanze
                for i in range(len(first_frame)):
                    if nameDist == "EUCLIDEAN":
                        # calcolo distanza euclidea PrimoFrame[cord.x,cord.y,cord.z] e FrameCorrente[cord.x,cord.y,cord.z]
                        dist = spatial.distance.euclidean(list(first_frame.iloc[i]), list(current_frame.iloc[i]))
                        distances.append(dist)
                    elif nameDist == "MANHATTAN":
                        # calcolo distanza manhattan PrimoFrame[cord.x,cord.y,cord.z] e FrameCorrente[cord.x,cord.y,cord.z]
                        dist = spatial.distance.cityblock(list(first_frame.iloc[i]), list(current_frame.iloc[i]))
                        distances.append(dist)
                # inserimento delle distanze nel csv SXXX_XXX (espresso precedentemente)
                # frame sulle righe e le distanze sulle colonne
                path_csv = os.path.join(path_globaldcsv,data[11:20]+namePath)
                f = open(path_csv, "a")
                writer = csv.writer(f)
                writer.writerow(distances)
                f.close()
    else:
         print("Nome distanza da calcolare errata!")

# calcolo della distanza euclidea
# distance_calc("GD_euclidean_csv", "GD_euclidean.csv", "EUCLIDEAN")

# calcolo della distanza di manhattan
# distance_calc("GD_manhattan_csv", "GD_manhattan.csv", "MANHATTAN")