import face_recognition # 얼굴 인식 라이브러리 (pip로 설치 가능)
import cv2 # 컴퓨터 비전 라이브러리 (OpenCV)
import numpy as np # 수치 계산을 위한 라이브러리

# 이 예제는 웹캠에서 실시간으로 얼굴 인식을 수행하는 데모입니다.
# 이 예제는 다음과 같은 기본적인 성능 개선 사항을 포함합니다:
#   1. 각 비디오 프레임을 1/4 해상도로 처리 (그러나 전체 해상도로 표시)
#   2. 매 프레임마다 얼굴을 감지하는 대신 매 다른 프레임마다 감지

# 주의: 이 예제는 웹캠에서 읽어오기 위해 OpenCV(cv2 라이브러리)가 필요합니다.
# face_recognition 라이브러리를 사용하기 위해 OpenCV가 반드시 필요한 것은 아닙니다.
# 설치에 문제가 있다면, OpenCV를 필요로 하지 않는 다른 예제를 시도해 보세요.

# 샘플 이미지를 불러오고 인식할 수 있도록 학습합니다.
obama_image = face_recognition.load_image_file("examples/obama.jpeg") # 오바마 이미지 파일 불러오기
obama_face_encoding = face_recognition.face_encodings(obama_image)[0] # 얼굴 인코딩 추출

# 두 번째 샘플 이미지를 불러오고 인식할 수 있도록 학습합니다.
biden_image = face_recognition.load_image_file("examples/biden.jpeg") # 바이든 이미지 파일 불러오기
biden_face_encoding = face_recognition.face_encodings(biden_image)[0] # 얼굴 인코딩 추출

# 인식된 얼굴 인코딩과 그에 해당하는 이름의 배열을 생성합니다.
known_face_encodings = [ # 인식된 얼굴 인코딩 리스트
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [ # 얼굴 인코딩에 해당하는 이름 리스트
    "Barack Obama",
    "Joe Biden"
]

# 몇 가지 변수를 초기화합니다.
face_locations = [] # 얼굴 위치를 저장할 리스트
face_encodings = [] # 얼굴 인코딩을 저장할 리스트
face_names = [] # 얼굴 이름을 저장할 리스트
process_this_frame = True # 프레임 처리 여부를 결정하는 변수

# 기본 웹캠(카메라 0번 장치) 참조 얻기
video_capture = cv2.VideoCapture(0)

while True:
    # 비디오의 단일 프레임을 가져옵니다.
    ret, frame = video_capture.read()

    # 얼굴 인식 처리를 빠르게 하기 위해 비디오 프레임 크기를 1/4로 조절합니다.
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # 프레임 크기 조절
    # 이미지를 BGR 색상(OpenCV에서 사용)에서 RGB 색상(face_recognition에서 사용)으로 변환합니다.
    rgb_small_frame = small_frame[:, :, ::-1]

    # 시간 절약을 위해 매 다른 프레임마다 처리합니다.
    if process_this_frame:
        # 현재 비디오 프레임에서 모든 얼굴과 얼굴 인코딩을 찾습니다.
        face_locations = face_recognition.face_locations(rgb_small_frame) # 얼굴 위치 찾기
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) # 얼굴 인코딩 찾기

        face_names = []
        for face_encoding in face_encodings:
            # 인식된 얼굴이 알려진 얼굴(들)과 일치하는지 확인합니다.
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding) # 얼굴 일치 여부 확인
            name = "Unknown" # 일치하는 얼굴이 없으면 "Unknown"으로 설정

            # # 알려진 얼굴 인코딩 중 첫 번째 일치 항목을 사용할 경우
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # 또는 새로운 얼굴과의 거리가 가장 작은 알려진 얼굴을 사용
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding) # 얼굴 거리 계산
            best_match_index = np.argmin(face_distances) # 가장 작은 거리의 인덱스 찾기
            if matches[best_match_index]: # 가장 작은 거리의 인덱스가 일치하는 경우
                name = known_face_names[best_match_index] # 해당 이름으로 설정

            face_names.append(name) # 얼굴 이름 리스트에 추가

    process_this_frame = not process_this_frame # 프레임 처리 여부 토글


    # 결과 표시
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # 얼굴 위치를 다시 원래 크기로 되돌립니다.
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 얼굴 주위에 상자를 그립니다.
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # 얼굴 아래에 이름 레이블을 그립니다.
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # 결과 이미지를 표시합니다.
    cv2.imshow('Video', frame)

    # 'q' 키를 누르면 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 핸들 해제
video_capture.release()
cv2.destroyAllWindows()
