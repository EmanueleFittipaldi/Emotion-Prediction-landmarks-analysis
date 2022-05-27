import os
import utils as utils
import cv2
from matplotlib import pyplot as plt
import pandas as pd

# Dataset path
path_dataset = "Dataset/cohn-kanade-images"
# Lables path
path_label = "Dataset/Emotion"

Dataset_folders = utils.get_directories(path_dataset=path_dataset)
Emotion_folders = utils.get_directories(path_dataset=path_label)

def process_landmarks(Dataset_folders):
    """
                    This function extracts all the landmarks from all the images contained in Dataset_folders

                   - **Returns**: nothing
                   - **Value return** has type none
                   - Parameter **Dataset_folders**:String value representing the path where all images are located
                   - **Precondition**: Dataset_folder must be a string value. Dataset must exist.
    """
    # loop nelle diverse cartelle per andare ad ottenere le singole immagini dei soggetti ed estrarre i landmark
    for dir in sorted(Dataset_folders):
        for img in os.listdir(dir):
            utils.extract_landmarks(dir,img)

def missing_emotion_labels():
    """
                    This function add missing emotion lables

                   - **Returns**: nothing
                   - **Value return** has type none
                   - Parameter **values**: none
                   - **Precondition**: Dataset must exist
    """

    # First of all, we obtain all the folders where there is no emotion label
    missing_EMlabels = [x for x in sorted(Emotion_folders) if len(x) == 0]

    # In order to be more efficient, we proceed to plotting the image of the subject to be labelled.
    # We can then enter the emotion label using the terminal. After a subject is manually labelled,
    # a new .txt is creaded, containing the emotion label.
    if len(missing_EMlabels) == 0:
        print("All lables added.")
    else:
        f = plt.figure()
        valueString = ".0000000e+00"
        for dir in Dataset_folders:
            for missing in missing_EMlabels:
                if dir.find(missing[16:]) != -1:
                    all_imges = sorted(os.listdir(dir))
                    image = cv2.imread(os.path.join(dir,all_imges[len(os.listdir(dir))-1]))
                    plt.imshow(image)
                    plt.show()
                    while(True):
                        val = input("Enter value of emotion: ")
                        if val != "":
                            filename = os.path.join(missing, all_imges[len(os.listdir(dir)) - 1].replace(".png","_emotion.txt"))
                            f = open(filename, 'w')
                            f.write(val + valueString)
                            f.close()
                            break

def missing_gender_labels():
    """
                    This function add missing gender lables

                   - **Returns**: nothing
                   - **Value return** has type
    """
    # In order to be more efficient, we proceed to plotting the image of the subject to be labelled.
    # We can then enter the Gender label using the terminal. After a subject is manually labelled,
    # a new .txt is creaded, containing the emotion label.
    for dir in sorted(Dataset_folders):
        all_imges = sorted(os.listdir(dir))
        filename = os.path.join(dir, all_imges[len(os.listdir(dir)) - 1]) \
            .replace("cohn-kanade-images", "Emotion") \
            .replace(".png", "_gender.txt")

        if not os.path.exists(filename):
            while (True):
                # Uomo = 0
                # Donna = 1
                val = input("Enter value of gender: ")
                if val != "" or val != 0 or val != 1:
                    f = open(filename, 'w')
                    f.write(val)
                    f.close()
                    break

def insert_labels_to_csv(path_label, path_GDcsv):
    """
                    This function adds Gender and Emotion lables csv as a new feature

                   - **Returns**: nothing
                   - **Value return** has type none
                   - Parameter **path_label**: String representing the path where the label is stored
                   - Parameter **path_GDcsv**: String representing the path where the Global distance csv
                     is stored.
                   - **Precondition**: All paths must be valid, and files existing.
        """
    dataset_labels = utils.get_directories(path_dataset=path_label)
    for dir in sorted(dataset_labels):
        for file in sorted(os.listdir(dir)):
            filename = os.path.join(dir, file)

            f = open(filename, "r")
            string_formatted = f.read().strip()
            f.close()

            csv = [c for c in os.listdir(path_GDcsv) if os.path.basename(c).startswith(file[:8])]
            df = pd.read_csv(os.path.join(path_GDcsv, csv), header=None)
            df[len(df.columns)] = string_formatted
            df.to_csv(os.path.join(path_GDcsv, csv), index=False, header=None)

# ----------------------------------------------------------------------------------------------------------------------
# CODE TO BE RUNNED ONLY ONCE
# process_landmarks(Dataset_folders)
missing_emotion_labels()
missing_gender_labels()
# insert_labels_to_csv("Dataset/Emotion", "Global_Distances")
# insert_labels_to_csv("Dataset/Emotion", "Local_Distances")



