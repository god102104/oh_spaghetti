from socket import *
from select import *
import config as cfg
import xhat as hw



### client end msg error

HOST = '192.168.219.108'
PORT = 5000
BUFSIZE = 1024
ADDR = (HOST, PORT)
serverSocket = socket(AF_INET, SOCK_STREAM)
IMGCenter = 320

serverSocket.bind(ADDR)
print('bind')
serverSocket.listen(100)
print('listen')

while(True):

  clientSocekt, addr_info = serverSocket.accept()

  data = clientSocekt.recv(65535)
  data = data.decode()
  print('recieve data : ',data)
  if data == "end":
    print("end")
    clientSocket.close()
    break;
  elif data == "noData":
    hw.motor_one_speed(0)
    hw.motor_two_speed(0)
  else:
    pet_center = float(data.split(";")[1])
    diff = pet_center - IMGCenter
    print(diff)
    if diff < -30 :
      #right
      hw.motor_one_speed(cfg.maxturn_speed)
      hw.motor_two_speed(0)
    elif diff > 30:
      #left
      hw.motor_one_speed(0)
      hw.motor_two_speed(cfg.maxturn_speed)
    else:
      hw.motor_one_speed(0)
      hw.motor_two_speed(0)
  clientSocket.close()

hw.motor_clean()

serverSocket.close()
print('close')

