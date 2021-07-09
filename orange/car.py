from socket import *
from select import *
import config as cfg
import xhat as hw
import sys
sys.path.append('../')
import user_setting as usr
import distance as ds

### client end msg error


#전체적인 내용은 bowl.py와 유사합니다.

BUFSIZE = 1024
#라즈베리 파이와 통신을 위한 소켓 설정
serverSocket = socket(AF_INET, SOCK_STREAM)
IMGCenter = 160 # 카메라 설정(320의 /2)

def motorSpeed(motor1, motor2):
  hw.motor_one_speed(motor1)
  hw.motor_two_speed(motor2)

serverSocket.bind(usr.ADDR)
print('bind')
serverSocket.listen(100)
print('listen')

maxspeed = cfg.maxturn_speed #car speed관련, config.py 를 참조.
minspeed = cfg.minturn_speed
clientSocket, addr_info = serverSocket.accept()

try:
 while(True):

  data = clientSocket.recv(65535)
  #if client socket close
  if not data:
   clientSocket.close()
   break
  data = data.decode()
  if data == "end":
    print("end")
    clientSocket.close()
    break
  # 거리 측정
  distance = ds.measure_average()
  print('distance:{}, recieve data :{}'.format(distance,data))

  # 30cm안에 물체가 있을 때 정지
  if distance <= 30:
    motorSpeed(0, 0)
    continue
  if data == "noData":
    # 물체를 찾지 못했을때 제자리에서 회전
    motorSpeed(cfg.firstMin, cfg.firstMax)
  else:
    temp = data.split(";")
    pet_center = float(temp[1].split(";")[0])# 인식된 대상의 width center 좌표
    diff = pet_center - IMGCenter
    if diff < -15 :
      #right
      motorSpeed(maxspeed, minspeed)
    elif diff > 15:
      #left
      motorSpeed(minspeed, maxspeed)
    elif diff>=-30 and diff<=30:
      motorSpeed(cfg.normal_speed_right, cfg.normal_speed_right)
    else:
      hw.motor_one_speed(0)
      hw.motor_two_speed(0)

except KeyboardInterrupt:
 hw.motor_clean()
 serverSocket.close()
 clientSocket.close()

hw.motor_clean()

serverSocket.close()
print('close')
