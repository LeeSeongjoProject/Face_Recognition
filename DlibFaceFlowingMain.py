from DlibFaceFlowingFace import face_detactor
from DlibFaceFlowingDrone import drone
import cv2

def main():
    # face_recongnition 과 tello drone 객체 생성
    face = face_detactor()
    drone_control = drone()

    # 드론 띄우기 및 드론 화면 활성화
    drone_control.set_drone()
    drone_control.take_off_drone()

    # 추적할 얼굴 데이터화
    face.encode_target_face()


    try:
        while True:

            # 드론 화면 가져오기
            img = drone_control.get_frame()

            # 드론 화면 크기 조절
            face.resize_frame(img)

            # 인식한 얼굴 확인
            face.detect_and_match_faces()
            xVal, yVal, zVal = face.chack_face()
            drone_control.tracking_face( xVal,  yVal,  zVal)
            face.show_frame()

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    #드론 착륙 및 모든 화면 종류
    drone_control.land_drone()
    face.all_end()

if __name__ == "__main__":
    main()
