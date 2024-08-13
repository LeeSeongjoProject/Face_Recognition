import cv2
import numpy as np
import face_recognition

#===이미지 로드===
# 이미지를 불러와서 등록(일론머스크)
imgElon = face_recognition.load_image_file('ImageBasic/musk.jpg')
# 카메라 색상이 RGB -> BGR로 변경
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)

# 이미지를 불러와서 등록(일론머스크_test_file)
imgElon_test = face_recognition.load_image_file('ImageBasic/musk2.jpeg')
# 카메라 색상이 RGB -> BGR로 변경
imgElon_test = cv2.cvtColor(imgElon_test, cv2.COLOR_BGR2RGB)

# 이미지를 불러와서 등록(빌게이츠)
imgBill = face_recognition.load_image_file('ImageBasic/billgates.jpg')
# 카메라 색상이 RGB -> BGR로 변경
imgBill = cv2.cvtColor(imgBill, cv2.COLOR_BGR2RGB)

#===이미지 분석===
# 일론머스크
# 이미지(얼굴) 파일의 특징을 튜플(top, right, bottom, left) 중 top을 반환
faceLoc = face_recognition.face_locations(imgElon)[0]
# 얼굴 인코딩을 사용하면 얼굴 간의 유사성을 계산하거나
# 이미 등록된 얼굴과 비교하여 식별할 수 있는 기능을 제공합니다
# 모든 얼굴에 대해 각각 얼굴 인코딩을 생성하여 리스트로 반환합니다
encodeElon = face_recognition.face_encodings(imgElon)[0]
# 이미지상의 직사각형 그리기
# cv2.rectangle(img, pt1, ptt2, color[, thickness[, lineType[, shift]]])
# rectangle 요약 : 이미지나 이미지 배열에 사각형을 그릴 때 유용하다
# img : 사각형을 그릴 이미지
# ((faceLoc[3], faceLoc[0]) / (faceLoc[1], faceLoc[2])) : 사각형의 (왼쪽 상단 / 오른쪽 하단) 꼭지점 좌표, (x, y) 형식의 튜플이여야 함
# (255, 0, 255) : 사각형의 색상
# 2 : 사각형의 두께(단위 px)
cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

# 일론머스크 테스트
faceLocTest = face_recognition.face_locations(imgElon_test)[0]
encodeElonTest = face_recognition.face_encodings(imgElon_test)[0]
cv2.rectangle(imgElon_test, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

#빌게이츠
faceLocBill = face_recognition.face_locations(imgBill)[0]
encodeBill = face_recognition.face_encodings(imgBill)[0]
cv2.rectangle(imgBill, (faceLocBill[3], faceLocBill[0]), (faceLocBill[1], faceLocBill[2]), (255, 0, 255), 2)

#===일치 결과 비교 (참거짓을 반환)===
# known_face_encodings : 비교할 얼굴
# face_encoding_to_check : 확인할 얼굴 128차원 벡터로 표현
# tolerance (선택사항) : 기본값은 0.6, 두 값이 같다고 생각하는 임계값
# 값이 작을수록 더 엄격해진다
results1 = face_recognition.compare_faces([encodeElon], encodeElonTest)
results2 = face_recognition.compare_faces([encodeElon], encodeBill)
print('일론 + 일론 테스트 : ', results1)
print('일론 + 빌 테스트 : ', results2)


#===이미지 출력===
# winname : 출력할 이미지 타이틀
# img name : 출력할 이미지
cv2.imshow('Elon Musk', imgElon)
cv2.imshow('Elon Musk test', imgElon_test)
cv2.imshow('Bill Gates', imgBill)
cv2.waitKey(0)
