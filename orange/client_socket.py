from socket import *
import os
import subprocess

flag = False
cp = 1
pat = "0\n"
flag = False
while True:
  ADDR = ('192.168.241.26',5050)
  clientSocket = socket(AF_INET, SOCK_STREAM)
  clientSocket.connect(ADDR)
  print("connect")
  
  data = clientSocket.recv(1024)
  data = data.decode()
  print(data)
  print(cp)
  if flag and past != data:
   print(cp.pid)
   os.system('sudo kill '+ str(cp.pid))
   print(cp.pid)
   continue
  if data=="1\n":
   flag = True
   print("Find")
   #cp1 = subprocess.Popen('sudo mjpg_streamer -i "input_uvc.so" -o "output_http.so -p 8081 -w /usr/local/share/mjpg-streamer/www/"', shell = True)
   cp = subprocess.Popen("python3 ~/oh_spaghetti/orange/car.py", shell = True)
  elif data == "2\n":
   flag = True
   cp = subprocess.Popen("python3 ~/oh_spaghetti/orange/bowl.py", shell = True) 
   print("check")
  elif data == "3\n":
   flag =True
   print("aircon")
  past = data
  clientSocket.close()

