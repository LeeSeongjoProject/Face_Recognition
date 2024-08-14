"""
작성자 : 최병권
작성일 : 2024 08 14
최종 편집일 : 2024 08 14

요약
    텔로드론과 페이스트레킹 기술을 이용하여 추적하는 AI 드론의 메인 코드

상세
    face_landmark_class 파일의 FaceTracking 클래스가 있어야 얼굴인식이 가능함
    드론 관련 조작키가 아직 추가 되지 않음
    향후 클래스로 추가할 예정
"""
from djitellopy import tello
import cv2
from face_landmark_class import FaceTracking

if __name__ == "__main__":
    face_tracker = FaceTracking("./faces/choi.jpg")

    me = tello.Tello()
    me.connect()
    print(me.get_battery())
    me.streamoff()
    me.streamon()

    while True:
        img = me.get_frame_read().frame
        img = cv2.resize(img, (640, 480))

        face_tracker.detect_and_match_faces(img)
        imgStacked = face_tracker.track_face(img)

        cv2.imshow("Image Stacked", imgStacked)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
