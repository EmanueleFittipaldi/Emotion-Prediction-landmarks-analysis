import pandas as pd
from scipy.stats import ttest_ind
import numpy as np
videoSequence = pd.read_csv("/Users/emanuelefittipaldi/PycharmProjects/Emotion_Prediction_Project/src/Local_Distances/S005_001_LD_euclidean.csv")
split = int(len(videoSequence)/2)
print(split)
# split del dataset
df_1 = videoSequence.iloc[:split,:]
df_2 = videoSequence.iloc[split:,:]

print("prima segmentazione")
print(df_1)
print("seconda segmentazione")
print(df_2)

# landmark1_df1_mean = df_1["0"].mean()
# landmark1_df2_mean = df_2["0"].mean()
#
# print("means")
# print(landmark1_df1_mean)
# print(landmark1_df2_mean)

res = ttest_ind(df_1["0"],df_2["0"])
print(res)