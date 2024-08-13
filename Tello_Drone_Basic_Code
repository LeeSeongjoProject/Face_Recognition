#Tello 드론 기본 코드 정리
from djitellopy import Tello #라이브러리에서 Tello 클래스 가져오기
import keyboard # 라이브러리 가져오기
		import time # 라이브러리 가져오기

tello = Tello() # tello 객체 생성
tello.connect() # tello 드론에 연결
print("Create Tello object")

battery_level = tello.get battery() #배터리 수명 레벨 출력
print(f"Battery Level: {battery_level}")

print("Takeoff!") 
tello.takeoff() # 드론 이륙 명령
#Command---------------------
print("Move up")
tello.move_up(40) # 드론을 40cm위로 상승
time.sleep(1) #해당초동안 대기

print("Move down")
tello.move_down(40) # 드론을 40cm아래로 하강
time.sleep(1) #해당초동안 대기

print("Move left")
tello.move_left(40) # 드론을 40cm 왼쪽으로 이동
time.sleep(1) # 해당초동안 대기

print("Move right") 
tello.move_right(40) # 드론을 40cm 오른쪽으로 이동
time.sleep(1)  # 해당초동안 대기

print("Move forward")
tello.move_forward(40) # 드론을 40cm 앞으로 이동
time.sleep(1) # 해당초동안 대기

print("Move backwards")
tello.move_back(40) # 드론을 40cm 뒤로 이동
time.sleep(1) # 해당초동안 대기

print("Rotate clockwise") 
tello.rotate_clockwise(90) # 시계 방향 회전  
time.sleep(1) # 해당초동안 대기

print("Rotate counter clockwise")
tello.rotate_counter_clockwise(90) # 반시계 방향 회전
time.sleep(1) # 해당초동안 대기

print("Flip right") 
tello.flip_right() #오른쪽으로 돌기
time.sleep(1)  # 해당초동안 대기
print("Flip left") 
tello.flip_left() #왼쪽으로 돌기
time.sleep(1)  # 해당초동안 대기
print("Flip forward")
tello.flip_forward() #앞으로 돌기
time.sleep(1)  # 해당초동안 대기
print("Flip back")
tello.flip_back() #뒤로 돌기
time.sleep(1)  # 해당초동안 대기
---------------------
#반복문 사용하기---------------------
#for i in range (0,3) :
	tello.move_up(30)
	tello.move_down(30)
	tello.move_left(30)
	tello.move_right(30) # 드론을 40cm 오른쪽으로 이동
	tello.move_forward(30) # 드론을 40cm 앞으로 이동
	tello.move_backwards(30) # 드론을 40cm 뒤로 이동
	tello.rotate_clockwise(90) # 시계 방향 회전 
	tello.rotate_counter_clockwise(90) # 반시계 방향 회전
---------------------
#함수정의하기---------------------
#def move_up_down(t):
	tello.move_up(t)
	tello.move_down(t)

#def move_left_light(t):
	tello.move_left(t)
	tello.move_right(t)
	
#def move_for_back_wards(t):
	tello.move_forward(t)
	tello.move_backwards(t)

#def move_rotate_wise(t):
	tello.move_clockwise(t)
	tello.move_counter_clockwise(t)

#def flip_left_right():
	tello.flip_right()
	tello.flip_left()
	
#def flip_for_backward():
	tello.flip_forward()
	tello.flip_forward()
---------------------
#Send_rc_control---------------------
print("Rc_control")
tello.send_rc_control(0,0,0,0)
left(-10)_right(10),forward(10)_backward(-10),up(10)_down(-10),clockwise(10),counterclockwise(-10)
# -100~100
---------------------
#Cross flight mission
tello.go_xyz_speed(0,0,0,0)
x (+)forward/(-)backwards
y (+)left/(-)right
z (+)up/(-)down

while True:
    if keyboard.is_pressed('t'):
        tello.takeoff()
    if keyboard.is_pressed('f'):
        tello.move_forward(100)
    if keyboard.is_pressed('r'):
        tello.rotate_counter_clockwise(130)
    if keyboard.is_pressed('b'):
        tello.move_back(100)
    if keyboard.is_pressed('s'):
        tello.land()
---------------------
    # CPU 사용량을 줄이기 위해 잠깐 대기
    time.sleep(0.1)
    
print("landing")
tello.land() #드론 착륙 명령
print("tocudwon... goodbye") # 착륙 완료 메시지 출력
