from djitellopy import Tello
import cv2
import threading


def get_command():
    while True:
        command = input("명령을 입력하세요 (1: 이륙, 2: 상승, 3: 하강, 4: 착륙, 기타: 종료): ")
        if command == '1':
            myTello.takeoff()
        elif command == '2':
            myTello.move_up(30)
        elif command == '3':
            myTello.move_down(30)
        elif command == '4':
            myTello.land()
        else:
            break


# 텔로 드론 초기화 및 연결
myTello = Tello()
myTello.connect()
myTello.streamon()  # 카메라 스트림 시작

# 배터리 수준 확인
battery_level = myTello.get_battery()
print(f"배터리 수준: {battery_level}")

# 명령 입력을 위한 스레드 시작
command_thread = threading.Thread(target=get_command)
command_thread.start()

while True:
    # 드론 카메라에서 프레임 읽기
    frame = myTello.get_frame_read().frame

    # 화이트 밸런스 조정 (필요에 따라 조정)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow('Tello Camera', frame)  # 컬러로 표시

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
myTello.streamoff()
cv2.destroyAllWindows()
print("드론 임무 완료!")
