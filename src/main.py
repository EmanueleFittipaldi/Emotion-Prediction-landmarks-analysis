import os
import mediap_util as mpu
import cv2
from multiprocessing import Pool, cpu_count

# path del dataset CK+
path_dataset = "/Users/paoloplomipc/PycharmProjects/Emotion_Prediction_Project/src/Dataset/cohn-kanade-images"

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
                    Dataset_folders.append(os.path.join(path_sdir,dir))

# sort dei path di tutte le cartelle
Dataset_folders = sorted(Dataset_folders)
print(Dataset_folders)

def process_landmarks(img):
    image = cv2.imread(img)
    num_faces, keypoints = mpu.TESS(image)
    f = open("Landmark.txt", "a")
    f.write("\nImage: {}, \nNumber of faces: {}, \nKeyPoints: {}".format(img, num_faces, keypoints))
    # print("\nImage: {}, \nNumber of faces: {}, \nKeyPoints: {}".format(path_image, num_faces, keypoints))
    f.close()

# loop nelle diverse cartelle per andare ad ottenere le singole immagini dei soggetti ed estrarre i landmark
for dir in Dataset_folders:
    for img in os.listdir(dir):
        path_image = os.path.join(dir, img)
        process_landmarks(path_image)

    # num_workers = 2
    # assert num_workers > 1, "Need more than 1 worker"
    # pool = Pool(processes=num_workers, maxtasksperchild=1)
    # pool.map_async(process_landmarks, [os.path.join(dir,img) for img in os.listdir(dir)])


