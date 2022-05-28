# Emotion Prediction - Landmarks Analysis
Team: Emanuele Fittipaldi, Paolo Plomitallo
_Università degli studi di Salerno, Fisciano, Salerno, Italy._

# Abstract
In the panorama of computer vision, the problem of emotion prediction has attracted more and more attention, as it places the emphasis on what happens from the occurrence of a micro-expression to the complete manifestation of a macro-expression. This study focused on analyzing the movement of facial landmarks obtained through the Mediapipe library, in order to understand the sequence of frames within a video sequence, in which a micro-expression takes place. The changes in the position of the landmarks were analyzed through statistical tests such as the p-value. The landmarks that proved to be significant were therefore counted in order to understand where in the video sequence there had been movement. For most individuals and expressions, the results indicate that in the initial frames there is the highest probability of finding a micro-expression. An inter-class and intra-class analysis was also conducted between the different subjects and different expressions. This analysis was carried out by comparing the similarity between the vectors of the distances of the landmarks in the last frame with respect to the initial frame and the similarity between the vectors of the significant landmarks belonging to the last frame. It emerged that the emotions associated with the "negative" sphere are very similar in terms of movement of the landmarks, obtaining similarities that are always very close.
