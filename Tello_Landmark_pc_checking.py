import face_recognition as face #
import cv2
import numpy as np

biden_image = face.load_image_file("./pitcture/biden.jpg") 
biden_face_encoding = face.face_encodings(biden_image)[0] 

obama_image = face.load_image_file("./pitcture/obama.jpg")
obama_face_encoding = face.face_encodings(obama_image)[0]

itzy_image = face.load_image_file("./doraemong/itzy.jpg")
itzy_face_encoding = face.face_encodings(itzy_image)[0]

itzy2_image = face.load_image_file("./pitcture/itzy2.jpeg")
itzy2_face_encoding = face.face_encodings(itzy2_image)[0]

karina_image = face.load_image_file("./pitctue01/musk.jpg")
karina_face_encoding = face.face_encodings(karina_image)[0]



first_face_encodings = [
    biden_face_encoding,
    obama_face_encoding,
    itzy2_face_encoding
]
first_face_names = [
    "biden",
    "obama",
    "itzy2"
]

seconed_face_encoding = [
    itzy_face_encoding,
    karina_face_encoding
]
seconed_face_name = [
    "itzy",
    "karina"
]
for face_encoding in first_face_encodings:
    matches = face.compare_faces(seconed_face_encoding, face_encoding, tolerance=0.5) #.compare=true false 값 변환. #toler = 얼굴 비교 기준. 이상시 유연하게 찾는다.but오류 이하시
    print(f'matches : {matches}')
    face_distances = face.face_distance(seconed_face_encoding, face_encoding)
    print(f'face_distances : {face_distances}')
    best_match_index = np.argmin(face_distances)
    print(f'best_match_index : {best_match_index}')
    print(f'matches[best_match_index] : {matches[best_match_index]}')
    if matches[best_match_index] > 0.5:
        name = seconed_face_name[best_match_index]
        print(f'seconed_face_name[best_match_index] : {seconed_face_name[best_match_index]}')
        print(f'name : {name}')
        #결과값
        # matches : [False, False] 
        # face_distances : [0.9271912 0.8183654]
        # best_match_index : 1
        # matches[best_match_index] : False
        # matches : [False, False]
        # face_distances : [1.02198241 0.88496004]
        # best_match_index : 1
        # matches[best_match_index] : False
        # matches : [True, False]
        # face_distances : [0.28346094 0.83672697]
        # best_match_index : 0
        # matches[best_match_index] : True
        # seconed_face_name[best_match_index] : itzy
        # name : itzy
        
     


