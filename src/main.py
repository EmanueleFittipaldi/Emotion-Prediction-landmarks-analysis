import os
import Helper as hp
import land_extractor as lext

# path del dataset CK+
path_dataset = hp.getFromEnv('DatasetPath')

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

# loop nelle diverse cartelle per andare ad ottenere le singole immagini dei soggetti ed estrarre i landmark
for dir in sorted(Dataset_folders):
    for img in os.listdir(dir):
        lext.process_landmarks(dir,img)

