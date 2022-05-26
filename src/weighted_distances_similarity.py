# from utils import *
# import pandas as pd
#
# Emotions = {1: "Anger",
#             2: "Contempt",
#             3: "Disgust",
#             4: "Fear",
#             5: "Happy",
#             6: "Sadness",
#             7: "Surprise"
#             }
#
# path_emotion = "Dataset/Emotion"
# Dataset_Emotion = get_directories(path_dataset=path_emotion)
# distance_name = "_GD_euclidean"
# distance_typedir = "Global_Distances/"
#
# # dizionario che mantiene le emozioni con i diversi soggetti,
# # quindi le chiavi sono le emozioni ed i valori tutti i soggetti di quella emozione
# emotion_dictionary = subjects_per_emotion(Dataset_Emotion=Dataset_Emotion, distance_name=distance_name)
#
# SPLIT_PERCENT = 0.8
# test_subjects = []
#
# # columns = { 1: [0.888355, 0.873252, 0.873308, 0.867073, 0.833290, 0.877848, 0.830290],
# #             2: [0.873252, 0.874211, 0.866920, 0.867197, 0.860873, 0.866558, 0.821439],
# #             3: [0.873308, 0.866920, 0.889282, 0.864420, 0.869549, 0.869607, 0.812009],
# #             4: [0.867073, 0.867197, 0.864420, 0.868243, 0.844843, 0.861261, 0.835643],
# #             5: [0.833290, 0.860873, 0.869549, 0.844843, 0.932606, 0.835797, 0.761870],
# #             6: [0.877848, 0.866558, 0.869607, 0.861261, 0.835797, 0.870114, 0.819227],
# #             7: [0.830290, 0.821439, 0.812009, 0.835643, 0.761870, 0.819227, 0.831948]
# #             }
# columns = {1: [0, 0, 0, 0, 0, 0, 0],
#            2: [0, 0, 0, 0, 0, 0, 0],
#            3: [0, 0, 0, 0, 0, 0, 0],
#            4: [0, 0, 0, 0, 0, 0, 0],
#            5: [0, 0, 0, 0, 0, 0, 0],
#            6: [0, 0, 0, 0, 0, 0, 0],
#            7: [0, 0, 0, 0, 0, 0, 0],
#            }
# df_weight = pd.DataFrame(columns, index=[1, 2, 3, 4, 5, 6, 7])
# df_weight = df_weight.astype(float)
#
# def mean_emotion_vector(emotion, distance_dir):
#     """
#             funzione che estrae per ogni emozione il vettore media di tutte le distanze globali tra i soggetti di quella emozione
#            - **Returns**:
#            - **Value return** has type
#            - Parameter **values**:
#            - **Precondition**:
#            """
#     emotion_subjects = emotion_dictionary[emotion]
#     training_emotion = emotion_subjects[:int(len(emotion_subjects) * SPLIT_PERCENT)]
#
#     testing_emotion = emotion_subjects[int(len(emotion_subjects) * SPLIT_PERCENT):]
#     test_subjects.append(testing_emotion)
#
#     emotion_distances = get_distances(distance_dir=distance_dir, emotion_subject=training_emotion)
#
#     df_emotion_distances = pd.DataFrame(emotion_distances).transpose()
#
#     meanVector = []
#     for i in range(0, 468):
#         meanVector.append(df_emotion_distances[int(i)].mean())
#
#     return meanVector
#
#
# def max_occurence(em_df, idxmax_value):
#     if idxmax_value[0] == idxmax_value[1] == idxmax_value[2]:
#         return idxmax_value[0]
#     elif idxmax_value[0] == idxmax_value[1] or idxmax_value[0] == idxmax_value[2]:
#         return idxmax_value[0]
#     elif idxmax_value[1] == idxmax_value[2]:
#         return idxmax_value[1]
#     else:
#         count_max_index = {}
#         count_max_index[idxmax_value[0]] = 0;
#         count_max_index[idxmax_value[1]] = 0;
#         count_max_index[idxmax_value[2]] = 0
#
#         for i in idxmax_value:
#             for j in range(1, 4):
#                 for z in idxmax_value:
#                     if i == z: continue
#                     v1 = em_df.iloc[i - 1]
#                     v2 = em_df.iloc[z - 1]
#                     if v1[j] > v2[j]:
#                         count_max_index[i] += 1
#
#         max_idx = max(count_max_index, key=count_max_index.get)
#
#         for key in count_max_index:
#             if count_max_index[key] == count_max_index[max_idx] and key != max_idx:
#                 v1 = em_df.iloc[max_idx - 1]
#                 v2 = em_df.iloc[key - 1]
#                 diff = 0
#                 for j in range(3):
#                     diff += v1[j+1] - v2[j+1]
#                 if diff > 0:
#                     return max_idx
#                 else:
#                     return key
#
#         return max_idx
#
#
# def emotion_prediction(emotions_meanVector, test_sub, distance_dir):
#     """
#             funzione che effettua una predizione dell'emozione su un soggetto preso a caso dal test set
#            - **Returns**:
#            - **Value return** has type
#            - Parameter **values**:
#            - **Precondition**:
#            """
#
#     em_predict = {}
#     meanVectorSim = {}
#
#     subject_distances = get_distances(distance_dir=distance_dir, emotion_subject=[test_sub])
#
#     for i in sorted(emotions_meanVector):
#         meanVectorSim['S' + str(i)] = vector_similarity(v1=subject_distances[test_sub[:8]], v2=emotions_meanVector[i])
#
#     value_c = min(meanVectorSim.values()) / 50
#     for i in meanVectorSim:
#         if i == max(meanVectorSim, key=meanVectorSim.get):
#             meanVectorSim[max(meanVectorSim, key=meanVectorSim.get)] += value_c
#         else:
#             meanVectorSim[i] -= value_c
#
#     for i in range(len(meanVectorSim)):
#         multi_diagonal = meanVectorSim['S' + str(i + 1)] * 100 * df_weight[i + 1][i + 1]
#         multi_weight = multi_diagonal
#
#         sim_mean_column = []
#         for j in range(len(df_weight.axes[0])):
#             sim_mean_column.append(meanVectorSim['S' + str(i + 1)] * 100 * df_weight[j + 1][i + 1])
#             if j == i: continue
#             multi_weight -= df_weight[j + 1][i + 1]
#
#         em_predict[i + 1] = [multi_diagonal, statistics.mean(sim_mean_column), multi_weight]
#
#     em_df = pd.DataFrame(em_predict, index=[1, 2, 3]).transpose()
#
#     highest_fc = em_df[1].nlargest(2).index.tolist();
#     highest_sc = em_df[2].nlargest(2).index.tolist();
#     highest_tc = em_df[3].nlargest(2).index.tolist()
#
#     emotion_predicted = []
#     for i in range(2):
#         idxmax_value = [highest_fc[i], highest_sc[i], highest_tc[i]]
#         emotion_predicted.append(max_occurence(em_df, idxmax_value))
#
#     emotion_subject_label = [key for key, val in emotion_dictionary.items() if any(test_sub[:8] in s for s in val)]
#     label = emotion_subject_label[0]
#
#     if label not in accuracy_per_emotion:
#         accuracy_per_emotion[label] = [0, 0]
#     if label in emotion_predicted:
#         accuracy_per_emotion[label][0] += 1
#         accuracy_per_emotion[label][1] += 1
#         return 1
#     else:
#         accuracy_per_emotion[label][1] += 1
#         return 0
# NUMBER_SPLIT = 10
# for n in range(NUMBER_SPLIT):
#
#     for i in range(7):
#         for j in range(7):
#             df_weight[i + 1][j + 1] = get_emotion_similarities(i + 1, j + 1, distance_typedir)
#     print("MATRICE SIM: \n", df_weight)
#
#
#     # estrazione vettori media distanze di ogni emozione
#     emotions_meanVector = {}
#     for i in range(7):
#         emotions_meanVector[i + 1] = mean_emotion_vector(emotion=i + 1, distance_dir=distance_typedir)
#     print("VETTORI DISTANZE MEDIE TRA EMOZIONI: \n", emotions_meanVector)
#
#     test_subjects = [item for sublist in test_subjects for item in sublist]
#
#
#     accuracy_per_emotion = {}
#     emotion_prediction_results = []
#     for s in test_subjects:
#         emotion_prediction_results.append(emotion_prediction(emotions_meanVector=emotions_meanVector,
#                                                              test_sub=s, distance_dir=distance_typedir))
#
#     success = emotion_prediction_results.count(1)
#     accuracy = (success / len(emotion_prediction_results)) * 100
# print("L'accuratezza è del: {:.2f} % \nIndovinate: {}/{}".format(accuracy, success, len(emotion_prediction_results)))
# print("Per ogni emozione sono state indovinate: ", accuracy_per_emotion)