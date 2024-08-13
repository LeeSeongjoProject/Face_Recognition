import cv2
import numpy as np
import face_recognition

def img_registration(img_name, img_src):
    # 이미지를 불러와서 등록(일론머스크) 텐서 값으로
    img = face_recognition.load_image_file(img_src)
    # 카메라 색상이 RGB -> BGR로 변경
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = img_analysis(img)
    return img, encode

def img_analysis(img_data):
    # 이미지(얼굴) 파일의 특징을 튜플(top, right, bottom, left) 중 top을 반환
    # 이미지에서 얼굴 위치를 반환한다
    faceLoc = face_recognition.face_locations(img_data)[0]
    # 얼굴 인코딩을 사용하면 얼굴 간의 유사성을 계산하거나
    # 이미 등록된 얼굴과 비교하여 식별할 수 있는 기능을 제공합니다
    # 모든 얼굴에 대해 각각 얼굴 인코딩을 생성하여 리스트로 반환합니다
    encode = face_recognition.face_encodings(img_data)[0]
    # 이미지상의 직사각형 그리기
    # cv2.rectangle(img, pt1, ptt2, color[, thickness[, lineType[, shift]]])
    # rectangle 요약 : 이미지나 이미지 배열에 사각형을 그릴 때 유용하다
    # img : 사각형을 그릴 이미지
    # ((faceLoc[3], faceLoc[0]) / (faceLoc[1], faceLoc[2])) : 사각형의 (왼쪽 상단 / 오른쪽 하단) 꼭지점 좌표, (x, y) 형식의 튜플이여야 함
    # (255, 0, 255) : 사각형의 색상
    # 2 : 사각형의 두께(단위 px)
    # 벡터 데이터로 반환
    cv2.rectangle(img_data, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
    return encode

def img_test(known_face_encodings, face_to_check_encoding, test_name, test_img):
    # ===일치 결과 비교 (참거짓을 반환)===
    # known_face_encodings : 비교할 얼굴
    # face_encoding_to_check : 확인할 얼굴 128차원 벡터로 표현
    # tolerance (선택사항) : 기본값은 0.6, 두 값이 같다고 생각하는 임계값
    # 값이 작을수록 더 엄격해진다
    results = face_recognition.compare_faces(known_face_encodings, face_to_check_encoding)
    print(test_name, results)

    # ===이미지 출력===
    # winname : 출력할 이미지 타이틀
    # img name : 출력할 이미지
    cv2.imshow(test_name, test_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 이미지 등록 및 인코딩
Elon_img, Elon_encoding= img_registration('Elon Musk', 'ImageBasic/musk.jpg')
Elon_test_img, Elon_test_encoding= img_registration('Elon Musk test', 'ImageBasic/musk2.jpeg')
bill_img, bill_encoding= img_registration('Bill Gates', 'ImageBasic/billgates.jpg')

# 얼굴 비교
img_test([Elon_encoding], Elon_test_encoding, 'Elon test', Elon_test_img)
img_test([Elon_encoding], bill_encoding, 'Bill test', bill_img)
