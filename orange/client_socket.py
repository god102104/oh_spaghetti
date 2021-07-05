from socket import *
import os

flag = False
while True:
  ADDR = ('172.30.1.11',5050)
  clientSocket = socket(AF_INET, SOCK_STREAM)
  clientSocket.connect(ADDR)
  print("connect")
  data = clientSocket.recv(1024)
  data = data.decode()
  print(data)
  if flag == True:
   continue
  if data=="1\n":
   flag = True
   print("Find")
   os.system("sudo sh ~/oh_spaghetti/orange/start.sh")
   os.system("sudo python3 ~/oh_spaghetti/orange/car.py")
  elif data == "2\n":
   flag = True
   os.system("sudo python3 ~/oh_spaghetti/orange/bowl.py > result2.txt")
   print("check")
  elif data == "3\n":
   flag = True
   print("aircon")
  clientSocket.close()

