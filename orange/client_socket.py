from socket import *
import os
import subprocess
import sys
import time
sys.path.append('..')
import user_setting as usr
flag = False
ADDR = (usr.Mobile, 5050)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)
past = "0\n"
print("connect")
while True:

  data = clientSocket.recv(1024)
  os.system("sudo fuser -k -n tcp 7000") #7000port 를 사용하는 프로세스를 강제종료. '찾아줘' 명령 이후 다음 작업에도 프로세스가 동작하여 문제가 발생하지 않도록
  data = data.decode()
  print(data)
  if data== "1\n" and data == past:
   continue
  if data=="1\n":
   print("Find")
 #  if data == "1\n" and not flag:
 #  os.system("sudo fuser -k -n tcp 4000")
   flag = True
 #  time.sleep(1)
   subprocess.Popen("python3 ~/oh_spaghetti/orange/car.py", shell = True)
  elif data == "2\n":
   flag = True
   os.system("sudo fuser -k -n tcp 4000")
   time.sleep(1)
   subprocess.Popen("python3 ~/oh_spaghetti/orange/bowl.py", shell = True) 
   print("Check")
   flag = False
  elif data == "3\n":
   flag = True
   print("Aircon")
   flag = False
  past = data

