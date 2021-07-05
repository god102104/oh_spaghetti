from socket import *
import os

flag = False
while True:
  ADDR = ('172.30.1.11',5050)
  clientSocket = socket(AF_INET, SOCK_STREAM)# 소켓을 생성한다.

  clientSocket.connect(ADDR)
  print("connect")
  data = clientSocket.recv(1024)
  data = data.decode()
  if flag == True:
   continue
  if data=="1\n":
   flag = True
   print("Find")
   os.system("python3 ~/oh_spaghetti/OD_with_socket.py")
  elif data == "2\n":
   flag = True
   os.system("rm ~/oh_spaghetti/result2.txt")
   os.system("python3 ~/oh_spaghetti/dog_bowl.py")
   f = open('~/oh_spaghetti/result2.txt', 'r')
   print(f.readline())

   print("check")
  elif data == "3\n":
   flag = True
   print("aircon")
  clientSocket.close()
