from socket import *
from select import *
import config as cfg
import xhat as hw
import sys
sys.path.append('../')
import user_setting as us
import distance as ds

### client end msg error

HOST = us.HOST
PORT = us.PORT
BUFSIZE = 1024
ADDR = (HOST, PORT)
serverSocket = socket(AF_INET, SOCK_STREAM)
IMGCenter = 160

def motorSpeed(motor1, motor2):
  hw.motor_one_speed(motor1)
  hw.motor_two_speed(motor2)

serverSocket.bind(ADDR)
print('bind')
serverSocket.listen(100)
print('listen')

maxspeed = cfg.maxturn_speed
minspeed = cfg.minturn_speed

try:
 while(True):

  clientSocket, addr_info = serverSocket.accept()

  data = clientSocket.recv(65535)
  data = data.decode()
  if data == "end":
    print("end")
    clientSocket.close()
    break
  distance = ds.measure_average()
  print('distance:{}, recieve data :{}'.format(distance,data))
  if distance <= 30:
    motorSpeed(0, 0)
    continue
  if data == "noData":
    motorSpeed(cfg.firstMin, cfg.firstMax)
  else:
    temp = data.split(";")
    pet_center = float(temp[1])
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
  clientSocket.close()

except KeyboardInterrupt:
 hw.motor_clean()
 serverSocket.close()

hw.motor_clean()

serverSocket.close()
print('close')