import os
import csv
import cv2
import mediap_util as mpu
import pandas as pd

def extract_landmarks(dir,img):
    filename = 'frames_csv/'+str(img)
    filename = filename.replace('.png', '.csv')

    # creazione file csv per la singola immagine
    f = open(filename, 'w')
    # creazione del writer per scrivere le righe nel csv
    writer = csv.writer(f)
    # colonne csv
    header = ['x','y','z']
    writer.writerow(header)

    # lettura immagine ed estrazione dei landmark
    image = cv2.imread(os.path.join(dir, img))
    num_faces, keypoints = mpu.TESS(image)

    # struttura dati che contiene i landmark divisi per righe (468x3)
    data = []
    for row in keypoints:
        data.append(row)
    # scrittura di tutte le righe nel csv
    writer.writerows(data)

    f.close()



