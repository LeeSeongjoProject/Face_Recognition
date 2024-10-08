from tkinter import Tk, Label, Button, filedialog, Frame
from PIL import Image, ImageTk
import cv2
import numpy as np
from djitellopy import tello
import cvzone
import face_recognition
import threading
import os
import webbrowser
import telegram
import asyncio

from cvzone.PIDModule import PID
from cvzone.PlotModule import LivePlot

# 얼굴 인식 결과를 표시할 때 사용할 폰트 설정
font = cv2.FONT_HERSHEY_DUPLEX
previous = "unknown"

# 드론 영상의 높이(hi)와 너비(wi) 설정
hi, wi = 480, 640

# PID 컨트롤러 설정 (각 축별로 제어)
xPID = PID([0.15, 0, 0.1], wi // 2)
yPID = PID([0.27, 0, 0.1], hi // 2, axis=1)
zPID = PID([0.005, 0, 0.003], 10000, limit=[-20, 15])

# PID 제어 결과를 실시간으로 플로팅하기 위한 설정 결과 표시
myPlotX = LivePlot(yLimit=[-100, 100], char='X')
myPlotY = LivePlot(yLimit=[-100, 100], char='Y')
myPlotZ = LivePlot(yLimit=[-100, 100], char='Z')

# 드론 객체 생성 및 연결
me = tello.Tello()
me.connect()
print(me.get_battery())  # 드론 배터리 상태 출력
me.streamoff()  # 스트리밍 종료 (이전에 켜져 있을 수 있으므로)
me.streamon()  # 드론에서 영상 스트리밍 시작

# 드론 이/착륙 상태 변수
is_flying = False

# 인식할 얼굴의 인코딩과 이름 배열을 생성 (빈 리스트로 초기화)
known_face_encodings = []
known_face_names = []

# 얼굴 인식 관련 변수 초기화
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Tkinter 창 설정
placeholder_image_path = "../images/empty.jpeg"  # 당신의 자리 표시자 이미지 파일 경로를 여기에 입력

# Tkinter 창 설정
root = Tk()
root.title("AI Drone for Saving Kids")
root.geometry("1130x487+200+100")  # 해상도, x-offset, y-offset

# 자리 표시자 이미지를 로드하여 173x217 크기로 조정
image_width, image_height = 173, 217  # 해상도 설정

placeholder_image = Image.open(placeholder_image_path)
placeholder_image = placeholder_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
placeholder_imgTk = ImageTk.PhotoImage(image=placeholder_image)

# 업로드된 얼굴을 표시하기 위한 Label 위젯 (자리 표시자로 기본 설정)
uploaded_face_label = Label(root, image=placeholder_imgTk)
uploaded_face_label.image = placeholder_imgTk  # 참조를 유지하여 이미지가 표시되도록 함
uploaded_face_label.place(x=645, y=1)  # 오른쪽 상단에 위치

# 영상 스트리밍을 표시할 Label 위젯을 정의
label = Label(root)
label.place(x=1, y=1)  # 웹캠 영상 표시를 위한 위치

# 구글 지도 API 삽입 - 예를 들어 구글 지도 웹페이지를 열 수 있는 버튼
# 구글 지도 API 삽입 - 예를 들어 구글 지도 웹페이지를 열 수 있는 버튼
image = Image.open("../images/heunde.png")  # 이미지 파일 경로
image = image.resize((480, 260))  # 이미지 크기 조정
photo = ImageTk.PhotoImage(image)

# 이미지 표시할 프레임
google_maps_frame = Frame(root, width=200, height=200)
google_maps_frame.place(x=643, y=218)  # 위치 설정

# 이미지 라벨
google_maps_label = Label(google_maps_frame, image=photo)
google_maps_label.pack()

# 이/착륙 기능을 비동기로 처리하는 함수
def toggle_takeoff_land():
    global is_flying
    if not is_flying:
        threading.Thread(target=takeoff_drone).start()
    else:
        threading.Thread(target=land_drone).start()

# 드론 이륙 함수
def takeoff_drone():
    global is_flying
    me.takeoff()
    is_flying = True
    root.after(0, lambda: takeoff_land_button.config(text="추적 중지", bg="red"))

# 드론 착륙 함수
def land_drone():
    global is_flying
    me.land()
    is_flying = False
    root.after(0, lambda: takeoff_land_button.config(text="추적 하기", bg="green"))

# 이미지 업로드 후 얼굴 이미지 위치 조정
def upload_image():
    global known_face_encodings, known_face_names, uploaded_face_label

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("JPEG files", "*.jpg"),
            ("JPEG files", "*.jpeg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("GIF files", "*.gif"),
            ("TIFF files", "*.tiff"),
            ("WEBP files", "*.webp"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        try:
            # 이미지 로드 및 얼굴 인코딩 처리
            new_image = face_recognition.load_image_file(file_path)
            new_face_encoding = face_recognition.face_encodings(new_image)[0]

            # 새로운 얼굴 인코딩과 이름 추가
            known_face_encodings.append(new_face_encoding)
            known_face_names.append("Target Found")
            print(f"New face added from {file_path}")

            # 업로드된 얼굴 이미지를 Tkinter 형식으로 변환하여 350x450 크기로 조정
            uploaded_image = Image.open(file_path)
            uploaded_image = uploaded_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
            imgTk = ImageTk.PhotoImage(image=uploaded_image)
            uploaded_face_label.config(image=imgTk)
            uploaded_face_label.image = imgTk  # 참조를 유지하여 이미지가 표시되도록 함
        except Exception as e:
            print(f"Error loading image: {e}")

# 업로드된 얼굴 이미지 삭제 함수
def delete_image():
    global known_face_encodings, known_face_names, uploaded_face_label

    if len(known_face_encodings) > 0:  # 리스트에 얼굴이 있는지 확인
        known_face_encodings.pop()  # 마지막으로 추가된 얼굴 인코딩 삭제
        known_face_names.pop()  # 마지막으로 추가된 얼굴 이름 삭제
        print("Last uploaded face deleted.")

        # 업로드된 얼굴 이미지를 자리 표시자 이미지로 대체
        uploaded_face_label.config(image=placeholder_imgTk)
        uploaded_face_label.image = placeholder_imgTk  # 참조를 유지하여 이미지가 표시되도록 함
    else:
        print("No uploaded face to delete.")

# 이/착륙 버튼 추가
takeoff_land_button = Button(root, text="미아 찾기", command=toggle_takeoff_land, font=("Helvetica", 20), width=9, height=4)
takeoff_land_button.place(x=976, y=2)

# 이미지 업로드 버튼 추가
upload_button = Button(root, text="사진 업로드", command=upload_image, font=("Helvetica", 20), width=9, height=4)
upload_button.place(x=822, y=2)

# 이미지 삭제 버튼 추가
delete_button = Button(root, text="사진 초기화", command=delete_image, font=("Helvetica", 20), width=9, height=4)
delete_button.place(x=822, y=111)
'''
def capture_image():
    # 드론에서 현재 프레임을 가져옴
    img = me.get_frame_read().frame
    if img is not None:
        # 자동 저장할 경로를 지정
        directory = "/Users/gim-yeongtaeg/Desktop/drone_image"  # 스크린샷 저장경로, 여기에 원하는 경로를 입력하세요
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 파일 이름 생성 (예: image_1.jpg, image_2.jpg 등)
        file_number = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]) + 1
        file_name = f"image_{file_number}.jpg"
        file_path = os.path.join(directory, file_name)

        # 이미지 저장
        cv2.imwrite(file_path, img)
        print(f"Captured image saved as {file_path}")
    else:
        print("Failed to capture image from drone.")
'''
# 텔레그램 봇 토큰과 채팅 ID (사용자 ID)
BOT_TOKEN = "7519420813:AAFvJida3Osw5hels7PBRs5fLgf-7vD2OCk"  # Telegram Bot API Token
CHAT_ID = "6270066372"  # 사용자 또는 그룹의 채팅 ID

# 텔레그램 봇 설정
bot = telegram.Bot(token=BOT_TOKEN)

# 비동기 함수: 그래픽이 포함된 이미지를 저장하고 텔레그램으로 전송
# 비동기 함수: 그래픽이 포함된 이미지를 저장하고 텔레그램으로 전송
async def capture_image_and_send():
    # 드론에서 현재 프레임을 가져옴
    img = me.get_frame_read().frame
    img = cv2.resize(img, (640, 480))  # 리사이즈
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 얼굴 인식 및 PID 제어 그래픽 포함 처리
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if name == "Unknown":
            continue

        results = face_recognition.face_landmarks(imgRGB)
        if len(results) != 0:
            cx = left + ((right - left) // 2)
            cy = top + ((bottom - top) // 2)
            area = (right - left) * (bottom - top)

            cv2.rectangle(imgRGB, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(imgRGB, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(imgRGB, name, (left + 6, bottom - 6), font, 1.0, (255, 0, 0), 1)

            xVal = int(xPID.update(cx))
            yVal = int(yPID.update(cy))
            zVal = int(zPID.update(area))

            # PID 드로잉만 적용 (그래프는 제외)
            imgRGB = xPID.draw(imgRGB, [cx, cy])
            imgRGB = yPID.draw(imgRGB, [cx, cy])
            imgRGB = zPID.draw(imgRGB, [cx, cy])

    # 텔레그램 전송을 위해 이미지 저장 (imgRGB에는 얼굴 인식 결과 및 그래픽만 포함)
    imgBGR = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)  # OpenCV는 BGR 형식을 사용하므로 다시 변환
    directory = "/Users/gim-yeongtaeg/Desktop/drone_image"  # 스크린샷 저장 경로
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 파일 이름 생성
    file_number = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]) + 1
    file_name = f"image_{file_number}.jpg"
    file_path = os.path.join(directory, file_name)

    # 이미지 저장
    cv2.imwrite(file_path, imgBGR)
    print(f"Captured image saved as {file_path}")

    # 텔레그램 메시지로 "타겟을 찾았습니다." 텍스트 전송 (비동기 처리)
    await bot.send_message(chat_id=CHAT_ID, text="타겟을 찾았습니다.")

    # 이미지 파일을 텔레그램으로 전송 (비동기 처리)
    with open(file_path, 'rb') as img_file:
        await bot.send_photo(chat_id=CHAT_ID, photo=img_file)
    print(f"Image sent to Telegram chat ID: {CHAT_ID}")

    # 경도와 위도 텍스트 추가
    location_text = f"타겟 위치: 위도 {35.1594965345398}, 경도 {129.162576586723}"
    await bot.send_message(chat_id=CHAT_ID, text=location_text)

    # 지도 이미지 파일 전송 (지도 사진 경로)
    map_file_path = "../images/heunde.png"  # 지도 이미지 경로
    with open(map_file_path, 'rb') as map_file:
        await bot.send_photo(chat_id=CHAT_ID, photo=map_file)
    print(f"Map image sent to Telegram chat ID: {CHAT_ID}")


# 동기 함수: 비동기 함수를 동기적으로 실행
def capture_image_and_send_sync():
    # asyncio.run()을 통해 비동기 함수를 동기적으로 호출
    asyncio.run(capture_image_and_send())


# 사진 촬영 버튼에서 동기 함수 실행
capture_button = Button(root, text="사진 전송", command=capture_image_and_send_sync, font=("Helvetica", 20), width=9, height=4)
capture_button.place(x=976, y=111)

# 드론의 현재 프레임을 캡처하여 저장하는 함수
def update_frame():
    global process_this_frame, face_locations, face_encodings, face_names

    # 드론에서 현재 프레임을 가져와서 리사이즈
    img = me.get_frame_read().frame
    img = cv2.resize(img, (640, 480))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if process_this_frame:
        face_locations = face_recognition.face_locations(imgRGB)
        face_encodings = face_recognition.face_encodings(imgRGB, face_locations)

        face_names = []
        if len(known_face_encodings) > 0:  # 인코딩 리스트가 비어 있지 않은 경우에만 비교 수행
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
                print(face_names)

    process_this_frame = not process_this_frame

    xVal = 0
    yVal = 0
    zVal = 0

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if name == "Unknown":
            continue

        results = face_recognition.face_landmarks(imgRGB)

        if len(results) != 0:
            cx = left + ((right - left) // 2)
            cy = top + ((bottom - top) // 2)
            area = (right - left) * (bottom - top)

            cv2.rectangle(imgRGB, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(imgRGB, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(imgRGB, name, (left + 6, bottom - 6), font, 1.0, (255, 0, 0), 1)

            xVal = int(xPID.update(cx))
            yVal = int(yPID.update(cy))
            zVal = int(zPID.update(area))

            print(xVal, yVal, zVal)
            print('area :', area)
            print('zVal', zVal)

            imgPlotX = myPlotX.update(xVal)
            imgPlotY = myPlotY.update(yVal)
            imgPlotZ = myPlotZ.update(zVal)

            imgRGB = xPID.draw(imgRGB, [cx, cy])
            imgRGB = yPID.draw(imgRGB, [cx, cy])
            imgRGB = zPID.draw(imgRGB, [cx, cy])

            imgStacked = cvzone.stackImages([imgRGB, imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)
        else:
            print("Face Not Found")
            imgStacked = cvzone.stackImages([imgRGB], 1, 0.75)
            cv2.putText(imgStacked, "Face Not Recognized", (-10, 50), font, 1.0, (255, 0, 255), 1)

        me.send_rc_control(0, -zVal, -yVal, xVal)

    imgPIL = Image.fromarray(imgRGB)
    imgTk = ImageTk.PhotoImage(image=imgPIL)

    label.config(image=imgTk)
    label.image = imgTk

    root.after(1, update_frame)

update_frame()

root.mainloop()
