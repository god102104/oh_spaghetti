from socket import *
from select import *
import config as cfg
import xhat as hw
import sys
sys.path.append('../')
import user_setting as us


def motorChange(motor1 = 0, motor2 = 0):
    hw.motor_one_speed(motor1)
    hw.motor_two_speed(motor2)

### client end msg error

HOST = us.HOST
PORT = us.PORT
BUFSIZE = 1024
ADDR = (HOST, PORT)
serverSocket = socket(AF_INET, SOCK_STREAM)
IMGCenter = 160

serverSocket.bind(ADDR)
print('bind')
serverSocket.listen(100)
print('listen')



try:
 dir = 1
 while(True):

  clientSocket, addr_info = serverSocket.accept()

  data = clientSocket.recv(65535)
  data = data.decode()
  print('recieve data : ',data)
  if data == "end":
    print("end")
    clientSocket.close()
    break;
  elif data == "noData":
    motorChange(cfg.firstMax, cfg.firstMin)
  else:
    temp = data.split(";")
    pet_center = float(temp[1])
    diff = pet_center - IMGCenter
    print("diff: " + str(diff))
    if diff < -15 :
      #right
      motorChange(cfg.maxturn_speed, cfg.minturn_speed)
    elif diff > 15:
      #left
      motorChange(cfg.minturn_speed, cfg.maxturn_speed)
    
#    elif diff>=-30 and diff<=30:
#      if float(temp[2]) <30:
#       hw.motor_one_speed(0)
#       hw.motor_two_speed(0)
#      else:
#       hw.motor_one_speed(cfg.normal_speed_right)
#       hw.motor_two_speed(cfg.normal_speed_left)
    else:
      motorChange(0,0)

  clientSocket.close()

except KeyboardInterrupt:
 hw.motor_clean()

hw.motor_clean()

serverSocket.close()
print('close')
