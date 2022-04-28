import os
import cv2
import mediapipe as mp
import itertools
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

#return number of faces and return coordinates of the left eye of the last one
def LEYE(sample_img):
  face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                         min_detection_confidence=0.5)
  face_mesh_results = face_mesh_images.process(sample_img[:, :, ::-1])

  ELEMENTS = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYE)))
  if face_mesh_results.multi_face_landmarks:

    for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

      num=face_no + 1
      keypoints = []
      for ITEM in ELEMENTS[:]:
        coord = face_landmarks.landmark[ITEM]
        keypoints.append([coord.x, coord.y, coord.z])
    return num, keypoints







#return number of faces and return coordinates of the right eye of the last one
def REYE(sample_img):
  face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                         min_detection_confidence=0.5)
  face_mesh_results = face_mesh_images.process(sample_img[:, :, ::-1])

  ELEMENTS = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYE)))
  if face_mesh_results.multi_face_landmarks:

    for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

      num=face_no + 1
      keypoints = []
      for ITEM in ELEMENTS[:]:
        coord = face_landmarks.landmark[ITEM]
        keypoints.append([coord.x, coord.y, coord.z])
    return num, keypoints




#return number of faces and return coordinates of the right eyebrow of the last one
def REYEB(sample_img):
  face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                         min_detection_confidence=0.5)
  face_mesh_results = face_mesh_images.process(sample_img[:, :, ::-1])

  ELEMENTS = list(set(itertools.chain(*mp_face_mesh.FACEMESH_RIGHT_EYEBROW)))
  if face_mesh_results.multi_face_landmarks:

    for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

      num=face_no + 1
      keypoints = []
      for ITEM in ELEMENTS[:]:
        coord = face_landmarks.landmark[ITEM]
        keypoints.append([coord.x, coord.y, coord.z])
    return num, keypoints



#return number of faces and return coordinates of the left eyebrow of the last one
def LEYEB(sample_img):
  face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                         min_detection_confidence=0.5)
  face_mesh_results = face_mesh_images.process(sample_img[:, :, ::-1])

  ELEMENTS = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LEFT_EYEBROW)))
  if face_mesh_results.multi_face_landmarks:

    for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

      num=face_no + 1
      keypoints = []
      for ITEM in ELEMENTS[:]:
        coord = face_landmarks.landmark[ITEM]
        keypoints.append([coord.x, coord.y, coord.z])
    return num, keypoints


#return number of faces and return coordinates of the lips of the last one
def LIPS(sample_img):
  face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                         min_detection_confidence=0.5)
  face_mesh_results = face_mesh_images.process(sample_img[:, :, ::-1])

  ELEMENTS = list(set(itertools.chain(*mp_face_mesh.FACEMESH_LIPS)))
  if face_mesh_results.multi_face_landmarks:

    for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

      num=face_no + 1
      keypoints = []
      print(ELEMENTS)
      for ITEM in ELEMENTS[:]:
        coord = face_landmarks.landmark[ITEM]
        keypoints.append([coord.x, coord.y, coord.z])
    return num, keypoints



#return number of faces and return coordinates of the border of the face of the last one
def OVAL(sample_img):
  face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                         min_detection_confidence=0.5)
  face_mesh_results = face_mesh_images.process(sample_img[:, :, ::-1])

  ELEMENTS = list(set(itertools.chain(*mp_face_mesh.FACEMESH_FACE_OVAL)))
  if face_mesh_results.multi_face_landmarks:

    for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

      num=face_no + 1
      keypoints = []
      for ITEM in ELEMENTS[:]:
        coord = face_landmarks.landmark[ITEM]
        keypoints.append([coord.x, coord.y, coord.z])
        print(ELEMENTS)
    return num, keypoints



#return number of faces and return coordinates of the contour of the elements of the face of the last one
def CONT(sample_img):
  face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                         min_detection_confidence=0.5)
  face_mesh_results = face_mesh_images.process(sample_img[:, :, ::-1])

  ELEMENTS = list(set(itertools.chain(*mp_face_mesh.FACEMESH_CONTOURS)))
  if face_mesh_results.multi_face_landmarks:

    for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

      num=face_no + 1
      keypoints = []
      print(ELEMENTS)
      for ITEM in ELEMENTS[:]:
        coord = face_landmarks.landmark[ITEM]
        keypoints.append([coord.x, coord.y, coord.z])
    return num, keypoints




#return number of faces and return coordinates of all the elements
def TESS(sample_img):
  face_mesh_images = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2,
                                         min_detection_confidence=0.5)
  face_mesh_results = face_mesh_images.process(sample_img[:, :, ::-1])

  ELEMENTS = list(set(itertools.chain(*mp_face_mesh.FACEMESH_TESSELATION)))
  if face_mesh_results.multi_face_landmarks:

    for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):

      num=face_no + 1
      keypoints = []
      # print(ELEMENTS)
      # print(len(ELEMENTS))
      for ITEM in ELEMENTS[:]:
        coord = face_landmarks.landmark[ITEM]
        keypoints.append([coord.x, coord.y, coord.z])
    return num, keypoints







