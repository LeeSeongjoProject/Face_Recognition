import face_recognition
import numpy as np
from cvzone.PIDModule import PID
from cvzone.PlotModule import LivePlot
import cv2
import cvzone
from DlibFaceFlowingDrone import drone
from cvzone.PIDModule import PID
from cvzone.PlotModule import LivePlot

class face_detactor:
    def __init__(self):
        # 얼굴 인식 결과를 표시할 때 사용할 폰트 설정(init)
        self.font = cv2.FONT_HERSHEY_DUPLEX

        # 드론 영상의 높이(hi)와 너비(wi) 설정
        self.wi, self.hi = 640, 480

        # PID 컨트롤러 설정 (각 축별로 제어)
        # xPID: 드론의 좌우(yaw) 제어
        self.xPID = PID([0.15, 0, 0.1], self.wi // 2)  # 0.22
        # yPID: 드론의 상하(up/down) 제어
        self.yPID = PID([0.27, 0, 0.1], self.hi // 2, axis=1)
        # zPID: 드론의 전후(forward/backward) 제어 (얼굴 영역의 크기에 따라)
        self.zPID = PID([0.005, 0, 0.003], 10000, limit=[-20, 15])  # 0.005, 35000

        # PID 제어 결과를 실시간으로 플로팅하기 위한 설정
        self.myPlotX = LivePlot(yLimit=[-100, 100], char='X')
        self.myPlotY = LivePlot(yLimit=[-100, 100], char='Y')
        self.myPlotZ = LivePlot(yLimit=[-100, 100], char='Z')

        drone_control = drone()
    def encode_target_face(self):
        # 대상 얼굴 이미지를 로드하고 얼굴 인코딩을 학습
        Target_image = face_recognition.load_image_file("faces/choi.jpg")

        Target_face_encoding = face_recognition.face_encodings(Target_image)[0]

        # 인식할 얼굴의 인코딩과 이름 배열을 생성
        self.known_face_encodings = [
            Target_face_encoding
        ]

        self.known_face_names = [
            "Target"  # 인식할 대상의 이름
        ]

    def resize_frame(self, img):
        self.img = img
        return cv2.resize(self.img, (self.wi, self.hi))

    def detect_and_match_faces(self):
        # 얼굴 인식 관련 변수 초기화
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []

        # 현재 프레임에서 얼굴 위치 및 인코딩을 찾음
        face_locations = face_recognition.face_locations(self.img)
        face_encodings = face_recognition.face_encodings(self.img, face_locations)

        for face_encoding in face_encodings:
            # 알려진 얼굴과 비교하여 매칭되는 얼굴 찾기
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.5)
            self.name = "Unknown"

            # 얼굴과의 거리(유사도)를 계산하여 가장 가까운 매칭 얼굴 선택
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                self.name = self.known_face_names[best_match_index]

            # 인식된 얼굴 이름을 face_names에 추가
            self.face_names.append(self.name)
            print(self.face_names)

    def chack_face(self):
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # PID 제어 변수 초기화(초기화가 필요한가?)
            xVal = 0
            yVal = 0
            zVal = 0
            # 이름이 "Unknown"이면 건너뛰기
            if not(self.name == "Unknown"):
                results = face_recognition.face_landmarks(self.img)
                xVal, yVal, zVal = self.PID(top, right, bottom, left, results)
                return xVal, yVal, zVal
        return xVal, yVal, zVal


    def PID(self, top, right, bottom, left, results):
        # 얼굴이 감지된 경우
        if len(results) != 0:
            # 얼굴 중심 좌표 계산
            cx = left + ((right - left) // 2)
            cy = top + ((bottom - top) // 2)

            # 얼굴 영역 크기 계산
            area = (right - left) * (bottom - top)

            self.face_name_set(top, right, bottom, left)

            # PID 제어를 통해 드론의 각 축별 이동값 계산
            xVal = int(self.xPID.update(cx))
            yVal = int(self.yPID.update(cy))
            zVal = int(self.zPID.update(area))

            # 제어 값 및 영역 크기 출력
            print('area :', area)
            print('xVal', xVal)
            print('yVal', yVal)
            print('zVal', zVal)

            # PID 제어 결과를 실시간으로 플롯
            imgPlotX = self.myPlotX.update(xVal)
            imgPlotY = self.myPlotY.update(yVal)
            imgPlotZ = self.myPlotZ.update(zVal)

            # 제어 값을 시각적으로 표시
            self.img = self.xPID.draw(self.img, [cx, cy])
            self.img = self.yPID.draw(self.img, [cx, cy])
            self.img = self.zPID.draw(self.img, [cx, cy])

            # 원본 영상과 PID 결과를 병합하여 표시
            imgStacked = cvzone.stackImages([self.img, imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)

            return xVal,yVal,zVal
        else:
            # 얼굴을 찾지 못한 경우 처리
            print("Face Not Found")
            imgStacked = cvzone.stackImages([self.img], 1, 0.75)
            cv2.putText(imgStacked, "Face Not Recognized", (-10, 50), self.font, 1.0, (255, 0, 255), 1)

    def face_name_set(self, top, right, bottom, left):
        # 얼굴 영역에 사각형과 이름을 표시
        cv2.rectangle(self.img, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(self.img, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(self.img, self.name, (left + 6, bottom - 6), self.font, 1.0, (255, 0, 0), 1)


    def show_frame(self):
        cv2.imshow("Face Recognition & Tracking", self.img)

    def all_end(self):
        # 모든 창 닫기
        cv2.destroyAllWindows()
