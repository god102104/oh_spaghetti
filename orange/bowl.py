from socket import *
from select import *
import config as cfg
import xhat as hw
import sys
sys.path.append('../')
import user_setting as usr
import distance as ds

### client end msg error

BUFSIZE = 1024
#라즈베리 파이와 통신을 위한 소켓 설정
serverSocket = socket(AF_INET, SOCK_STREAM)
IMGCenter = 160 # 카메라 설정(320의 /2)

def motorSpeed(motor1, motor2):
  hw.motor_one_speed(motor1)
  hw.motor_two_speed(motor2)

serverSocket.bind(usr.ADDR2)
print('bind')
serverSocket.listen(100)
print('listen')

maxspeed = cfg.maxturn_speed
minspeed = cfg.minturn_speed

clientSocket, addr_info = serverSocket.accept()

try:
 while(True):

  data = clientSocket.recv(65535) #recevied data 저장
  #if client socket close
  if not data:
   clientSocket.close() 
   break
  data = data.decode() 
  #물체 인식 후 움직일 필요가 없기에 socket close
  if data == "end": 
    print("end")
    clientSocket.close()
    break
  
  #ds.measuer_average()를 통해 3번의 초음파센서 위치 측정값의 평균으로 거리를 잡음.
  distance = ds.measure_average() 
  print('distance:{}, recieve data :{}'.format(distance,data)) 
  if distance <= 30: #distance 가 30cm보다 같거나 작으면 모터를 정지.
    motorSpeed(0, 0)
    ss = "Find"
    clientSocket.send(ss.encode()) #find라는 문자열을 encoding하여 socket으로 send
    break 
  if data == "noData":
    motorSpeed(cfg.firstMin, cfg.firstMax) #data를 찾지 못했을 경우 계속해서 이동
  else:
    temp = data.split(";") #받은 데이터를 ;를 기준으로 분리. clientSocket.send((data_[0]+";"+str(data_[1])).encode())과 같은 형식으로 통신하므로 data[0]과 data[1]을 따로 얻기위함.
    pet_center = float(temp[1]) #data[1]을 물체의 center 값으로 이용. 
    diff = pet_center - IMGCenter #diff = 중앙값과 이미지 출력창의 중앙값의 차이를 저장
    if diff < -15 : # diff가 -15 -> 물체가 왼쪽으로 치우쳐있으므로 우측 이동 
      #right
      motorSpeed(maxspeed, minspeed)
    elif diff > 15: #diff 가 15 -> 물체가 오른쪽으로 치우쳐있으므로 좌측 이동
      #left
      motorSpeed(minspeed, maxspeed)
    elif diff>=-30 and diff<=30: # abs(diff) =< 30일 경우, 좌우의 모터속도를 일치시켜 전진
      motorSpeed(cfg.normal_speed_right, cfg.normal_speed_right)
    else:
      hw.motor_one_speed(0)
      hw.motor_two_speed(0)
  ss = "Not Find"
  clientSocket.send(ss.encode()) 

except KeyboardInterrupt:
 hw.motor_clean()
 serverSocket.close()
 clientSocket.close()

hw.motor_clean()

serverSocket.close()
print('close')
