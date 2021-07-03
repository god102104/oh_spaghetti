from socket import *
from select import *
import config as cfg
import xhat as hw



### client end msg error

#HOST = '172.30.1.43'
HOST = '192.168.219.100'
PORT = 5000
BUFSIZE = 1024
ADDR = (HOST, PORT)
serverSocket = socket(AF_INET, SOCK_STREAM)
IMGCenter = 320

serverSocket.bind(ADDR)
print('bind')
serverSocket.listen(100)
print('listen')

flag = False
try:
 while(True):

  clientSocket, addr_info = serverSocket.accept()

  data = clientSocket.recv(65535)
  data = data.decode()
  print('recieve data : ',data)
  if float(data) <50:
    hw.motor_one_speed(0)
    hw.motor_two_speed(0)
  else:
    hw.motor_one_speed(cfg.normal_speed_right)
    hw.motor_two_speed(cfg.normal_speed_left)
  clientSocket.close()

except KeyboardInterrupt:
 hw.motor_clean()

hw.motor_clean()

serverSocket.close()
print('close')
