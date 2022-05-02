import os
def getDirectories(path_dataset):
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
                        Dataset_folders.append(os.path.join(path_sdir, dir))
    return Dataset_folders
