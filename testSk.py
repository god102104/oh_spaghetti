from socket import *
import subprocess
import os
import threading, requests, time
 
def sendData(sc):
    sc.send("find".end())
 
t1 = threading.Thread(target=getHtml, args=('http://google.com',))
t1.start()
flag = False
#while True:
ADDR = ('172.30.1.50',5050)
clientSocket = socket(AF_INET, SOCK_STREAM)# 소켓을 생성한다.

clientSocket.connect(ADDR)
print("connect")
data = clientSocket.recv(1024)
data = data.decode()
print(data)
if data=="Find\n":
 flag = True
 print("Find")
 t = threading.Thread(target=sendData, args=(clientSocket))
 t.start()
 # clientSocket.close()