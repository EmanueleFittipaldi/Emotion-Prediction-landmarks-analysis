import os
from scipy import spatial
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

# Per verificare se due sequenze di numeri sono simili utilizziamo il concetto di similarità del coseno
def vectorSimilarity(v1,v2):
    return 1 - spatial.distance.cosine(v1, v2)


# vec1 = [114, 122, 128, 133, 157, 158, 159, 168, 173, 188, 189, 190, 193,243, 244, 245,28,364, 365, 367, 379, 394, 397, 430, 434, 56, 8,0,0,0,0]
# vec2 = [100, 101, 118, 119, 120, 123, 18, 251, 264, 265, 276, 283, 293, 300, 301, 313,340,345, 346, 347,353,356, 368, 372, 383, 389, 446, 447, 47, 50, 83]
# vec3 = [100, 105, 107, 114, 126, 128, 133, 142, 189, 190, 193, 205, 209, 217, 221, 222, 223, 224, 233, 243, 244, 27, 28, 280, 29, 352, 355, 371, 376, 47, 50]
# vec1= sorted(vec1)
# vec2 = sorted(vec2)
# print(vectorSimilarity(vec2,vec3))