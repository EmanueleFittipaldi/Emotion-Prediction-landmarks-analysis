import os
import Helper as hp
import land_extractor as lext
import utils
import cv2
from matplotlib import pyplot as plt
# path del dataset CK+
path_dataset = hp.getFromEnv('DatasetPath')
# path label
path_label = hp.getFromEnv('LabelPath')

def processLandmarks(Dataset_folders):
    # loop nelle diverse cartelle per andare ad ottenere le singole immagini dei soggetti ed estrarre i landmark
    for dir in sorted(Dataset_folders):
        for img in os.listdir(dir):
            lext.process_landmarks(dir,img)

Dataset_folders = utils.getDirectories(path_dataset)
# processLandmarks(Dataset_folders)
Emotion_folders = utils.getDirectories(path_label)
# print(Emotion_folders)

missing_label = []
for dir in sorted(Emotion_folders):
    if len(os.listdir(dir)) == 0:
        missing_label.append(dir)

f = plt.figure()
for dir in Dataset_folders:
    for missing in missing_label[125:]:
        if dir.find(missing[16:]) != -1:
            all_imges = sorted(os.listdir(dir))
            image = cv2.imread(os.path.join(dir,all_imges[len(os.listdir(dir))-1]))
            plt.imshow(image)
            plt.show()
            while(True):
                val = input("Enter your value: ")
                if val != "":
                    print(val+".0000000e+00")
                    f = open(os.path.join(missing, all_imges[len(os.listdir(dir)) - 1].replace(".png","_emotion.txt")), 'w')
                    f.write(val+".0000000e+00")
                    f.close()
                    break